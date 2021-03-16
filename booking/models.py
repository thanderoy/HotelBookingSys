from django.db import models

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
    