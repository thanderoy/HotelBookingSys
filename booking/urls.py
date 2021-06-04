from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

app_name = 'booking'

urlpatterns = [
    path('daraja/stk-push', csrf_exempt(stk_push_callback), name='mpesa_stk_push_callback'),
    
    path('', RoomListView, name='RoomListView'),
    path('booking_list/', BookingListView.as_view(), name='BookingListView'),
    path('room/<category>/', RoomDetailView.as_view(), name='RoomDetailView'),
    path('booking/cancel/<pk>', CancelBookingView.as_view(), name='CancelBookingView'),
    path('checkout/<category>/', CheckoutView, name='CheckoutView'),
    path('pdf_download/', ReceiptDownloadView.as_view(), name='ReceiptDownloadView'),

]

