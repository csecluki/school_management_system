import random
from django.db.models import Avg

from users.management.commands.populate_database import PopulateCommand

from grades.models import Grade, EndGrade
from users.models import User
from courses.models import CourseGroup


class Command(PopulateCommand):
    help = 'Populate the grades_endgrade table with sample data. '
    
    def populate(self):
        config = self.config.get('endgrade', {})
        distribution = config.get('distribution_parameters')
        EndGrade.objects.all().delete()
        mean_values = Grade.objects.values('student', 'course_group').annotate(mean_value=Avg('value'))
        for mean_data in mean_values:
            adjusted_mean = mean_data['mean_value'] + random.triangular(*distribution)
            rounded_adjusted_mean = round(adjusted_mean * 2) / 2
            EndGrade.objects.create(
                student=User.objects.get(id=mean_data['student']),
                course=CourseGroup.objects.get(id=mean_data['course_group']).course,
                value=min(rounded_adjusted_mean, 6.0) if rounded_adjusted_mean != 1.5 else 1.0
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully populated grades_endgrade. '))
