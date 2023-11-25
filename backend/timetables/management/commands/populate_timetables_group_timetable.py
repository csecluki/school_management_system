import random

from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from timetables.models import GroupTimeTable, LessonUnit
from courses.models import CourseGroup


class Command(BaseCommand):
    help = 'Populate the timetabes_group_timetable table with sample data'

    def handle(self, *args, **kwargs):
        GroupTimeTable.objects.all().delete()
        
        lesson_units = LessonUnit.objects.all()

        for course_group in CourseGroup.objects.all():
            while True:
                try:
                    GroupTimeTable.objects.create(
                        course_group=course_group,
                        day_of_week=random.choice(GroupTimeTable.WEEK_DAYS)[0],
                        lesson_unit=random.choice(lesson_units)
                    )
                except ValidationError:
                    pass
                else:
                    break

        self.stdout.write(self.style.SUCCESS(f'Successfully created GroupTimeTable instances. '))
