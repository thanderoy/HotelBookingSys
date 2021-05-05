from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, FormView, View
from django.urls import reverse
from .models import *
from .forms import *
from booking.booking_func.availability import check_availability

# Create your views here.

def RoomListView(request):
    room = Room.objects.all()[0]
    room_categories = dict(room.ROOM_CATEGORIES)
    # print('categories = ', room_categories)

    room_values = room_categories.values()
    # print('categories = ', room_values)

    room_list = []

    for category in room_categories:
        room = room_categories.get(category)
        # print(room)
        room_url = reverse('booking:RoomDetailView', kwargs={'category':category})
        # print(room, room_url)

        room_list.append((room, room_url))


    context = {
        'room_list': room_list,
    }
    # print(room_list)
    return render(request, 'home.html', context)

class BookingList(ListView):
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
        form = AvailabilityForm()
        room_list = Room.objects.filter(category=category)
        

        if len(room_list) > 0:
            room = room_list[0]
            room_category = dict(room.ROOM_CATEGORIES).get(room.category, None)
            context = {
                'category':room_category,
                'form':form
            }

            return render(request, 'detail.html', context)
        else:
            return HttpResponse("Category Nyet!")
        
        


    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        room_list = Room.objects.filter(category=category)
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

        available_rooms = []
        for room in room_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)

        if len(available_rooms) > 0:
            room = available_rooms[0]
            booking = Booking.objects.create(
                user = self.request.user,
                room = room,
                check_in = data['check_in'],
                check_out = data['check_out']
            )
            booking.save()
            return HttpResponse(booking)

        else:
            return HttpResponse("Fukk! We're out of those rooms" )
        
class BookingView(FormView):
    form_class = AvailabilityForm
    template_name = 'booking/availability.html'
    

    def form_valid(self, form):
        data = form.cleaned_data
        room_list = Room.objects.filter(category=data['category'])
        