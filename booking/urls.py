from django.urls import path
from .views import *

app_name = 'booking'

urlpatterns = [
    path('room_list/', RoomListView, name='RoomListView'),
    path('booking_list/', BookingList.as_view(), name='BookingList'),
    path('book/', BookingView.as_view(), name='BookingView'),
    path('room/<category>/', RoomDetailView.as_view(), name='RoomDetailView'),
]

