from django.shortcuts import render, HttpResponse
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




# Create your views here.

def RoomListView(request):
    room_list = get_room_list()
    # room_details = get_room_details()
    

    
        

    context = {
        'room_list': room_list,
        # 'room_details': room_details
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
        form = AvailabilityForm()

        if got_category is not None:
            
            context = {
                'category':got_category,
                'form':form
            }

            return render(request, 'detail.html', context)
        else:
            return HttpResponse("Category Nyet!")
    
        

    # def post(self, request, *args, **kwargs):
    #     category = self.kwargs.get('category', None)
    #     form = AvailabilityForm(request.POST)

        
    #     if form.is_valid():
    #         data = form.cleaned_data
        
    #     available_rooms = get_available_rooms(category, data['check_in'], data['check_out'] )



    #     if available_rooms is not None:
    #         booking = book_room(request, available_rooms[0], data['check_in'], data['check_out'])
            
    #         return HttpResponse(booking)
    #     else:
    #         return HttpResponse("Fukk! We're out of those rooms" )

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

def CheckoutView(request, self):

        category = self.kwargs.get('category', None)
        form = AvailabilityForm(request.POST)

        
        if form.is_valid():
            data = form.cleaned_data
        
        available_rooms = get_available_rooms(category, data['check_in'], data['check_out'] )

        if available_rooms is not None:

            room = available_rooms[0]

        else:
            HttpResponse("Room Not Available")

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
        
