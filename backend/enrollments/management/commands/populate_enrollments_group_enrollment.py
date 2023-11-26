import random

from django.core.management.base import BaseCommand

from courses.models import CourseGroup
from enrollments.models import GroupEnrollment, RecruitmentStrategy


class Command(BaseCommand):
    help = 'Populate the enrollments_group_enrollment table with sample data'

    def handle(self, *args, **kwargs):
        GroupEnrollment.objects.all().delete()
        course_groups = CourseGroup.objects.all()
        recruitment_strategy = RecruitmentStrategy.objects.all()

        for course_group in course_groups:
            GroupEnrollment.objects.create(
                course_group=course_group,
                max_students=self.get_limit(),
                recruitment_strategy=random.choices(recruitment_strategy, weights=(0.7, 0.3))[0]
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully created GroupEnrollment instances. '))
    
    @staticmethod
    def get_limit():
        r = random.random()
        if r < 0.6:
            return random.randint(16,40)
        if r < 0.85:
            return random.randint(40, 250)
        return random.randint(3, 16)
