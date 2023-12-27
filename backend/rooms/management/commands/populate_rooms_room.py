import random
from django.db import transaction
from rooms.models import Room
from users.management.commands.populate_database import PopulateCommand


class Command(PopulateCommand):
    help = 'Populate the rooms_room table with sample data'

    def handle(self, *args, **options):
        self.config = self.load_config(options.get('config'), 'rooms')
        with transaction.atomic():
            self.populate_rooms()
    
    def populate_rooms(self):
        Room.objects.all().delete()

        room_numbers = self.room_numbers()

        for rn in room_numbers:
            Room.objects.create(
                room_number=rn,
                capacity=self.get_capacity()
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully populated rooms_room. '))
    
    def room_numbers(self):
        while True:
            rooms_on_floors = [
                    random.randint(
                        self.config.get('min_rooms_per_floor'),
                        self.config.get('max_rooms_per_floor')
                    )
                        for _ in range(self.config.get('floors'))
                ]
            if sum(rooms_on_floors) == self.config.get('total_rooms'):
                return self.create_room_numbers(rooms_on_floors)

    def get_capacity(self):
        return random.choices(
            list(self.config.get('capacity_choices').keys()),
            weights=list(self.config.get('capacity_choices').values())
        )[0]
    
    @staticmethod
    def create_room_numbers(floors):
        return [f"{floor}{str(n + 1).zfill(2)}" for floor, rooms in enumerate(floors) for n in range(rooms)]
