from django.shortcuts import redirect, render, HttpResponse
from django.views.generic import ListView, FormView, View, DeleteView
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
import json
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

        print(category)
        print(got_category)
        
        form = AvailabilityForm()

        if got_category is not None:
            
            context = {
                'category':got_category,
                'form':form
            }

            return render(request, 'detail.html', context)
        else:
            return HttpResponse("Category Nyet!")
    
        

    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        form = AvailabilityForm(request.POST)

        
        if form.is_valid():
            data = form.cleaned_data

            
        
            available_rooms = get_available_rooms(category, data['check_in'], data['check_out'] )



            if available_rooms is not None:

                room = available_rooms[0]

                context = {
                    'room':room

                }
            
                return render(request, 'booking/checkout.html', context)
        else:
            return HttpResponse("Fukk! We're out of those rooms" )
    
        
class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking_cancel.html'
    success_url = reverse_lazy('booking:BookingListView')

class CheckoutView(View):

    def get(self, *args, **kwargs):

        form = PhoneNoForm()

        context= {
            'form': form
        }

        return render(self.request, 'booking/chekout.html', context)

    def post(self, *args, **kwargs):

        form = PhoneNoForm(self.request.POST or None)

        if form.is_valid():
            phone_no = form.cleaned_data.get('PhoneNo')

            print(phone_no)
            return phone_no

        else:
            form = PhoneNoForm()

        return redirect('booking:RoomDetailView')
    
    
    # return render(request, 'booking/checkout.html')
        
        

def PaymentCompleteView(request):
    body = json.loads(request.body)
    print('BODY:', body)
    return JsonResponse('Payment Received', safe=False)


# class BookingView(FormView):
#     form_class = AvailabilityForm
#     template_name = 'booking/availability.html'
    

#     def form_valid(self, form):
#         data = form.cleaned_data
#         room_list = Room.objects.filter(category=data['category'])
        
def MpesaCheckoutView(request):
    cl = MpesaClient()
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt
    phone_number = '0790906416'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = 'https://darajambili.herokuapp.com/express-payment'

    # callback_url = request.build_absolute_uri(reverse('booking:mpesa_stk_push_callback'))
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

    return HttpResponse(response.text)

def stk_push_callback(request):
    data = request.body
    # You can do whatever you want with the notification received from MPESA here.
