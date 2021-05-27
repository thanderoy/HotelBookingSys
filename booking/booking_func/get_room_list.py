from booking.models import Room
from django.urls import reverse
from booking.booking_func.get_room_details import get_room_details

def get_room_list():
    room = Room.objects.all()[0]
    room_categories = dict(room.ROOM_CATEGORIES)
    # print('categories = ', room_categories)

    room_cat_list = []
    room_details_list = []
    

    for category in room_categories:
        room = room_categories.get(category)
        # print(room_cat)
        room_url = reverse('booking:RoomDetailView', kwargs={'category':category})
        # print(room, room_url)
        room_cat_list.append((room, room_url))

        room_detail = get_room_details(category)
        room_details_list.append(room_detail)
        # print(room_detail.capacity)

    data_list = list(zip(room_cat_list, room_details_list))
    
    # print(data_list)
    
    return data_list
    