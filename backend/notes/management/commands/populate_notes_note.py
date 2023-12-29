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
        notes = self.get_note_range(note_range)
        for student, group in student_group:
            for _ in range(int(random.triangular(*distribution))):
                Note.objects.create(
                    student=student,
                    course_group=group,
                    value=random.choice(notes)
                )
        self.stdout.write(self.style.SUCCESS(f'Successfully populated notes_note. '))

    def get_note_range(self, note_range):
        low, high = note_range
        r = [i * 0.5 for i in range(low * 2, high * 2 + 1)]
        r.remove(1.5)
        return r
