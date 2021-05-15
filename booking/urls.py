from django.urls import path
from .views import *

app_name = 'booking'

urlpatterns = [
    path('room_list/', RoomListView, name='RoomListView'),
    path('booking_list/', BookingListView.as_view(), name='BookingListView'),
    path('room/<category>/', RoomDetailView.as_view(), name='RoomDetailView'),
    path('booking/cancel/<pk>', CancelBookingView.as_view(), name='CancelBookingView'),
    path('checkout/', CheckoutView, name='CheckoutView'),
    path('complete_payment/', PaymentCompleteView, name='PaymentCompleteView')
]

