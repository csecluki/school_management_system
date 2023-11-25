from django.core.management.base import BaseCommand
from timetables.models import LessonUnit


class Command(BaseCommand):
    help = 'Populate the timetables_lesson_unit table with sample data'

    def handle(self, *args, **kwargs):
        LessonUnit.objects.all().delete()

        data = [
            {'id': 1, 'start_time': '08:00:00', 'end_time':'09:30:00' },
            {'id': 2, 'start_time': '09:45:00', 'end_time':'11:15:00' },
            {'id': 3, 'start_time': '11:30:00', 'end_time':'13:00:00' },
            {'id': 4, 'start_time': '13:30:00', 'end_time':'15:00:00' },
            {'id': 5, 'start_time': '15:15:00', 'end_time':'16:45:00' },
            {'id': 6, 'start_time': '17:00:00', 'end_time':'18:30:00' },
            {'id': 7, 'start_time': '18:45:00', 'end_time':'20:15:00' },
        ]

        for unit in data:
            LessonUnit.objects.create(**unit)

        self.stdout.write(self.style.SUCCESS(f'Successfully created LessonUnit instances. '))
