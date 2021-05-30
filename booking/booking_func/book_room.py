from booking.models import Booking

def book_room(user, room, check_in, check_out):
    booking = Booking.objects.create(

        user = user,
        room = room,
        check_in = check_in,
        check_out = check_out,
    )
    booking.save()

    return booking