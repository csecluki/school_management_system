import random
from users.management.commands.populate_database import PopulateCommand

from notes.models import Note
from users.models import User


class Command(PopulateCommand):
    help = 'Populate the notes_note table with sample data. '
    
    def populate(self):
        config = self.config.get('note', {})
        distribution = config.get('triangular_distribution_parameters')
        note_range = config.get('note_range')
        Note.objects.all().delete()
        student_group = [
            (student, group)
            for student in User.objects.filter(groups__name="Students")
            for group in student.enrolled_groups.all()
        ]
        for student, group in student_group:
            for _ in range(int(random.triangular(*distribution))):
                Note.objects.create(
                    student=student,
                    course_group=group,
                    value=random.choice(range(*note_range))
                )
        self.stdout.write(self.style.SUCCESS(f'Successfully populated notes_note. '))
