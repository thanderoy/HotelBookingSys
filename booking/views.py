from django.shortcuts import redirect, render, HttpResponse
from django.views.generic import ListView, View, DeleteView
from django.urls import reverse, reverse_lazy
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

class BookingListView(ListView):
    model = Booking 

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
        # Use a Safaricom phone number that you have access to, for you to be able to view the prompt
        phone_number = phone_no
        # amount = price
        amount = 1
        account_reference = 'reference'
        transaction_desc = 'Description' 
        # callback_url = 'https://darajambili.herokuapp.com/express-payment'
        callback_url = 'https://end9m3so3m5u9.x.pipedream.net/'
        response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

        print('Processing payment...')

        str_response = response.text
        print(str_response)
        dict_response = json.loads(str_response)

        
        # return HttpResponse(str_response)
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
        
    

def stk_push_callback(request):
    response = requests.get('https://end9m3so3m5u9.x.pipedream.net/', hooks=)
    
    print('*******')
    print(response.text)
    print('*******')
    print(response.status_code)


    return render(request, 'booking/paymentcomplete.html', {'response':response})
    # You can do whatever you want with the notification received from MPESA here.
