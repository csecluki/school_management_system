import random
from django.db.models import Avg

from users.management.commands.populate_database import PopulateCommand

from notes.models import Note, EndNote
from users.models import User
from courses.models import CourseGroup


class Command(PopulateCommand):
    help = 'Populate the notes_endnote table with sample data. '
    
    def populate(self):
        config = self.config.get('endnote', {})
        distribution = config.get('distribution_parameters')
        EndNote.objects.all().delete()
        mean_values = Note.objects.values('student', 'course_group').annotate(mean_value=Avg('value'))
        for mean_data in mean_values:
            adjusted_mean = mean_data['mean_value'] + random.triangular(*distribution)
            rounded_adjusted_mean = round(adjusted_mean * 2) / 2
            EndNote.objects.create(
                student=User.objects.get(id=mean_data['student']),
                course=CourseGroup.objects.get(id=mean_data['course_group']).course,
                value=min(rounded_adjusted_mean, 6.0) if rounded_adjusted_mean != 1.5 else 1.0
            )
        self.stdout.write(self.style.SUCCESS(f'Successfully populated notes_endnote. '))
