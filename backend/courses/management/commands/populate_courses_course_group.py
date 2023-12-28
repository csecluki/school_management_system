import random
from django.http import Http404

from django.shortcuts import get_object_or_404

from users.management.commands.populate_database import PopulateCommand
from timetables.models import Period
from courses.models import Course, CourseGroup


class Command(PopulateCommand):
    help = 'Populate the courses_course_group table with sample data'

    def populate(self):
        config = self.config.get('course_group', {})
        period = self.get_period(config.get('period', None))
        randomizer = config.get('randomizer', {})

        CourseGroup.objects.all().delete()

        for course in Course.objects.all():
            course_counter = 0
            if random.random() > randomizer.get(str(course_counter), 1):
                CourseGroup.objects.create(
                    course=course,
                    period=period
                )
                course_counter += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully populated courses_course_group. '))
    
    @staticmethod
    def get_period(period_id):
        try:
            return get_object_or_404(Period, id=period_id)
        except Http404:
            return Period.objects.order_by('id').first()
