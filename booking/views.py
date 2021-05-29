from django.shortcuts import redirect, render, HttpResponse
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, View, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
import json

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

        print('Room requested by User: ' + got_category)

        room_detail = get_room_details(category)
        
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

            room = available_rooms[0]


            request.session['room'] = room
            request.session['check_in'] = data['check_in']
            request.session['check_out'] = data['check_out']

            if available_rooms is not None:

                room = available_rooms[0]
                print('Room available. Redirecting to payment...')

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
        account_reference = 'reference'
        transaction_desc = 'Description' 
        # callback_url = request.build_absolute_uri(reverse('booking:mpesa_stk_push_callback'))
        callback_url = 'https://dcad15fecaaa.ngrok.io/daraja/stk-push'
        # callback_url = 'https://end9m3so3m5u9.x.pipedream.net/'
        # callback_url = 'https://4576b4f15e41.ngrok.io'
        
        response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

        print(' ')
        print('Processing payment...')

        str_response = response.json()
        response_code = str_response['ResponseCode']
        mpesa_response = str_response['ResponseDescription']
        customer_response = str_response['CustomerMessage']

        print('')
        print('ResponseCode: ', response_code)
        print(mpesa_response)
        print(customer_response)
        print('')

        
        return HttpResponse('Processing payment...')
        # return redirect('booking:mpesa_stk_push_callback')

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

    data = request.body
    body = json.loads(data)
    result_code = body['Body']['stkCallback']['ResultCode']
    result_desc = body['Body']['stkCallback']['ResultDesc']

    print(' ')
    print('ResultCode: ', result_code)
    print(result_desc)
    print(' ')

    


    return HttpResponse(data)

    

# HTTP Listener for MPESA results on Callback URL
from flask import Flask,jsonify, make_response, request 
  
app = Flask(__name__)

@app.route('/daraja/stk-push', methods=['POST'])
def webhook():
    request_data = request.data
    
    return request_data


if __name__ == '__main__':
    app.run(debug=True)