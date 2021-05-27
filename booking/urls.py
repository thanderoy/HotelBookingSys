from django.urls import path
from .views import *

app_name = 'booking'

urlpatterns = [
    path('room_list/', RoomListView, name='RoomListView'),
    path('booking_list/', BookingListView.as_view(), name='BookingListView'),
    path('room/<category>/', RoomDetailView.as_view(), name='RoomDetailView'),
    path('booking/cancel/<pk>', CancelBookingView.as_view(), name='CancelBookingView'),
    path('checkout/<category>/', CheckoutView, name='CheckoutView'),

    path('daraja/stk-push', stk_push_callback, name='mpesa_stk_push_callback'),

]

