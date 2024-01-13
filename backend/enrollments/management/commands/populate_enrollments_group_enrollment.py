import random

from django.core.management.base import CommandError

from courses.models import CourseGroup
from enrollments.models import GroupEnrollment, RecruitmentStrategy
from users.management.commands.populate_database import PopulateCommand


class Command(PopulateCommand):
    help = 'Populate the enrollments_group_enrollment table with sample data'

    def populate(self):
        config = self.config.get('group_enrollment')
        period = self.get_period(config.get('period', None))
        limits = config.get('student_limit', {})
        strategy_weights = config.get('strategy_weights', [])
        recruitment_strategy = RecruitmentStrategy.objects.all()
        if len(strategy_weights) != len(recruitment_strategy):
            raise CommandError(f"Number of strategies doesn't match weights number. ")
        GroupEnrollment.objects.all().delete()
        course_groups = CourseGroup.objects.filter(period=period)

        for course_group in course_groups:
            max_students = self.get_limit(limits)
            GroupEnrollment.objects.create(
                course_group=course_group,
                max_students=max_students,
                recruitment_strategy=random.choices(recruitment_strategy, weights=strategy_weights)[0],
                min_students=max_students * 0.3
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully populated enrollments_group_enrollment. '))
    
    @staticmethod
    def get_limit(limits):
        r = random.random()
        key = max(float(x) for x in limits if float(x) < r)
        return random.choice(range(*limits[str(key)]))
