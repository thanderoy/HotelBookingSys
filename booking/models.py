from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.
class Room(models.Model):
    ROOM_CATEGORIES = (
        ('BZS', 'BUSINESS SUITE'),
        ('TNS', 'TWIN SUITE'),
        ('EXS', 'EXECUTIVE SUITE'),
        ('SGB', 'SINGLE BED'),
    )
    room_number = models.IntegerField()
    category = models.CharField(choices=ROOM_CATEGORIES, max_length=3)
    beds = models.IntegerField()
    capacity = models.IntegerField()

    def __str__(self):
        return f'{self.room_number}.{self.category} with {self.beds} bed(s) for {self.capacity} person(s)' 
    
class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

    def __str__(self):
        return f'{self.user} has booked {self.room} from {self.check_in} to {self.check_out}'

    def get_category(self):
        categories = dict(self.room.ROOM_CATEGORIES)
        category = categories.get(self.room.category)
        return category

    def cancel_booking(self):
        return reverse('booking:CancelBookingView', args=[self.pk, ])

    