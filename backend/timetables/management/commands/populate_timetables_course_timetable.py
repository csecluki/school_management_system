import random

from django.core.management.base import BaseCommand
from schedules.models import ClassSchedule, SeasonSchedule, LessonUnitTime
from classes.models import Class
from rooms.models import Room


class Command(BaseCommand):
    help = 'Populate the schedules_class_schedule table with sample data'

    def handle(self, *args, **kwargs):
        ClassSchedule.objects.all().delete()

        lesson_units = LessonUnitTime.objects.all()
        rooms = Room.objects.all()

        for class_ in Class.objects.all():
            for season in SeasonSchedule.objects.all():
                ClassSchedule.objects.create(
                    day_of_week=random.choice(ClassSchedule.WEEK_DAYS)[0],
                    class_instance=class_,
                    lesson_unit = random.choice(lesson_units),
                    season_schedule=season,
                    room=self.get_room(class_, rooms)
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully created ClassSchedule instances. '))

    @staticmethod
    def get_room(class_, rooms):
        while True:
            room = random.choice(rooms)
            if room.capacity >= class_.limit:
                return room
