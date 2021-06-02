from django.shortcuts import redirect, render, HttpResponse
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, View, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime
import json
import time

import requests
from .models import *
from .forms import *
from booking.booking_func.availability import check_availability
from booking.booking_func.get_room_list import get_room_list
from booking.booking_func.get_room_category import get_room_category
from booking.booking_func.get_available_rooms import get_available_rooms
from booking.booking_func.book_room import book_room
from booking.booking_func.get_room_details import get_room_details
from django_daraja.mpesa.core import MpesaClient





# Create your views here.

def RoomListView(request):
    room_list = get_room_list()
        

    context = {
        'room_list': room_list,
    }
    # print(room_list)
    return render(request, 'home.html', context)

class BookingListView(LoginRequiredMixin, ListView):
    model = Booking 
    login_url = '/accounts/login/'


    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list

class RoomDetailView(View):

    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)

        got_category = get_room_category(category)

        print('')
        print('Room requested by User: ' + got_category)
        print('')

        room_detail = get_room_details(category)

        global room_detail_val
        def room_detail_val():
            return room_detail

        
        
        form = AvailabilityForm()

        if got_category is not None:
            
            context = {
                'room_details': room_detail,
                'category':got_category,
                'form':form
            }

            return render(request, 'detail.html', context)
        else:
            return HttpResponse("Category Nyet!")
    
        

    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        form = AvailabilityForm(request.POST)

        got_category = get_room_category(category)

        
        if form.is_valid():
            data = form.cleaned_data
        
            available_rooms = get_available_rooms(category, data['check_in'], data['check_out'] )

            check_in = data['check_in']
            check_out = data['check_out']

            global in_val
            def in_val():
                return check_in

            global out_val
            def out_val():
                return check_out

            print('')
            print('In: ', check_in, '   Out: ', check_out)
            print('')

            if available_rooms is not None:

                room = available_rooms[0]

                global room_val
                def room_val():
                    return room

                global user_val
                def user_val():
                    return request.user

                print('Room available. Redirecting to payment...')
                print('')

                context = {
                    'room':room,
                    'category': got_category
                }
                
                return redirect('booking:CheckoutView', category=category)
                # return render(request, 'booking/checkout.html', context)
            else:
                return HttpResponse("We're out of those rooms" )
        else:
            category = self.kwargs.get('category', None)
            got_category = get_room_category(category)

            context = {
                'category':got_category,
                'form':form
            }

            return render(request, 'detail.html', context)
        
        
class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking_cancel.html'
    success_url = reverse_lazy('booking:BookingListView')

@login_required
def CheckoutView(request, category):
    # template_name = 'booking/checkout.html'
    if request.method == 'POST':
        phone_no = request.POST.get("PhoneNo")
        got_category = get_room_category(category)

        room_detail = get_room_details(category)
        price = int(room_detail.price)

        cl = MpesaClient()
        
        phone_number = phone_no
        # amount = price
        amount = 1
        account_reference = 'Hotelio Room Booking'
        transaction_desc = 'Description' 
        # callback_url = request.build_absolute_uri(reverse('booking:mpesa_stk_push_callback'))
        callback_url = 'https://a5245d5bf84e.ngrok.io/daraja/stk-push'
        response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

        print(' ')
        print('Processing payment...')

        str_response = response.json()

        response_code = str_response['ResponseCode']
        mpesa_response = str_response['ResponseDescription']
        customer_response = str_response['CustomerMessage']

        print('')
        print('ResponseCode: ', response_code)
        print('MPESA Response: ', mpesa_response)
        print('Customer Response: ', customer_response)
        print('')

        time.sleep(15)        
        # return HttpResponse('Processing payment...')
        return redirect('booking:mpesa_stk_push_callback')

    else:
        form = PhoneNoForm()

        got_category = get_room_category(category)

        room_detail = get_room_details(category)

        context = {
            'room_details': room_detail,
            'category':got_category,
            'form': form
        }

        return render(request, 'booking/checkout.html', context)
        

@csrf_exempt
def stk_push_callback(request):

    try:
        data = request.body
        print(data)

        got_data = json.loads(data.decode("utf-8"))

        result_code = got_data['Body']['stkCallback']['ResultCode']
        result_desc = got_data['Body']['stkCallback']['ResultDesc']

        global result_code_val
        def result_code_val():
            return result_code

        print(' ')
        print('ResultCode: ', result_code)
        print(result_desc)
        print(' ')

    except Exception:
        pass
    
    result_code = result_code_val()
    
    if result_code == 0:
        room = room_val()
        check_in = in_val()
        check_out = out_val()
        user = user_val()

        booking = book_room(user, room, check_in, check_out)
        print (booking)
        
        return HttpResponse('Rooom booked')
        # return redirect('booking:PayCompleteView')

    else:
        print('Room not booked')
        return HttpResponse('Error in payment')
        # return redirect('booking:PayErrorView')
        # return render(request, 'booking/paymenterror.html')


    

# HTTP Listener for MPESA results on Callback URL
from flask import Flask,jsonify, make_response, request 
  
app = Flask(__name__)

@app.route('/daraja/stk-push', methods=['POST'])
def webhook():
    request_data = request.data
    
    return request_data


if __name__ == '__main__':
    app.run(debug=True)