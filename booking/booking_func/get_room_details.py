from booking.models import Room
from django.urls import reverse

def get_room_details(category):
    
    category_list = []

    room_det = Room.objects.filter(category=category)[0]
    category_list.append(room_det)
    # print(category_list)
    room_detail = category_list[0]

    return room_detail
        

