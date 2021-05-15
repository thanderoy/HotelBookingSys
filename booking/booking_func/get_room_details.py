from booking.models import Room
from django.urls import reverse

def get_room_details(*args, **kwargs):
    room = Room.objects.all()[0]
    room_categories = dict(room.ROOM_CATEGORIES)
    # print('categories = ', room_categories)

    room_details_list = []
    

    for category in room_categories:
        room = room_categories.get(category)
        # print(room)
        category_list = []
        room_det = Room.objects.filter(category=category)[0]
        category_list.append(room_det)
        # print(category_list)
        room_details = category_list[0]
        room_details_list.append(room_details)
        # print(room_details.capacity)

    return room_details_list