from booking.models import Room
from django.urls import reverse

def get_room_list():
    room = Room.objects.all()[0]
    room_categories = dict(room.ROOM_CATEGORIES)
    # print('categories = ', room_categories)

    room_cat_list = []

    for category in room_categories:
        room = room_categories.get(category)
        # print(room)
        room_url = reverse('booking:RoomDetailView', kwargs={'category':category})
        # print(room, room_url)

        room_cat_list.append((room, room_url))

    return room_cat_list