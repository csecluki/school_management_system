from django.db import models

class Room(models.Model):

    room_number = models.CharField(max_length=3, unique=True)
    capacity = models.PositiveSmallIntegerField()

    class Meta:
        default_permissions = ()

    def __str__(self):
        return f"Room {self.room_number}"
