import random
from users.management.commands.populate_database import PopulateCommand

from grades.models import Grade
from users.models import User


class Command(PopulateCommand):
    help = 'Populate the grades_grade table with sample data. '
    
    def populate(self):
        config = self.config.get('grade', {})
        distribution = config.get('triangular_distribution_parameters')
        grade_range = config.get('grade_range')
        Grade.objects.all().delete()
        student_group = [
            (student, group)
            for student in User.objects.filter(groups__name="Students")
            for group in student.enrolled_groups.all()
        ]
        grades = self.get_grade_range(grade_range)
        for student, group in student_group:
            for _ in range(int(random.triangular(*distribution))):
                Grade.objects.create(
                    student=student,
                    course_group=group,
                    value=random.choice(grades)
                )
        self.stdout.write(self.style.SUCCESS(f'Successfully populated grades_grade. '))

    def get_grade_range(self, grade_range):
        low, high = grade_range
        r = [i * 0.5 for i in range(low * 2, high * 2 + 1)]
        r.remove(1.5)
        return r
