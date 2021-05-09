from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, FormView, View, DeleteView
from django.urls import reverse, reverse_lazy
from .models import *
from .forms import *
from booking.booking_func.availability import check_availability
from booking.booking_func.get_room_list import get_room_list
from booking.booking_func.get_room_category import get_room_category
from booking.booking_func.get_available_rooms import get_available_rooms
from booking.booking_func.book_room import book_room



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
            booking = book_room(request, available_rooms[0], data['check_in'], data['check_out'])
            
            return HttpResponse(booking)
        else:
            return HttpResponse("Fukk! We're out of those rooms" )
        
class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking_cancel.html'
    success_url = reverse_lazy('booking:BookingListView')



# class BookingView(FormView):
#     form_class = AvailabilityForm
#     template_name = 'booking/availability.html'
    

#     def form_valid(self, form):
#         data = form.cleaned_data
#         room_list = Room.objects.filter(category=data['category'])
        
