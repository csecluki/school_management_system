import random
from django.core.management.base import BaseCommand
from rooms.models import Room


class Command(BaseCommand):
    help = 'Populate the rooms_room table with sample data'

    FLOORS = 3
    ROOM_PER_FLOOR = 15
    MIN_ROOMS_PER_FLOOR = 5
    TOTAL_ROOMS = 30
    CAPACITY_CHOICES = {6: 0.06, 15: 0.2, 24: 0.15, 36: 0.45, 48: 0.1, 120: 0.1, 250: 0.04}

    def handle(self, *args, **kwargs):
        Room.objects.all().delete()

        room_numbers = self.room_numbers()

        for rn in room_numbers:
            room = Room.objects.create(
                room_number=rn,
                capacity=self.get_capacity()
            )
            self.stdout.write(self.style.SUCCESS(f'Room {room.room_number} created. '))
    
    def room_numbers(self):
        while True:
            r = [random.randint(self.MIN_ROOMS_PER_FLOOR, self.ROOM_PER_FLOOR) for _ in range(self.FLOORS)]
            if sum(r) == self.TOTAL_ROOMS:
                return self.create_room_numbers(r)

    def get_capacity(self):
        return random.choices(
            list(self.CAPACITY_CHOICES.keys()),
            weights=list(self.CAPACITY_CHOICES.values())
        )[0]
    
    @staticmethod
    def create_room_numbers(floors):
        return [f"{floor}{str(n + 1).zfill(2)}" for floor, rooms in enumerate(floors) for n in range(rooms)]
