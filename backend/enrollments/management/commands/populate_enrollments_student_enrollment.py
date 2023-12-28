import random

from django.db.models import Sum
from users.management.commands.populate_database import PopulateCommand
from rest_framework.exceptions import ValidationError

from users.models import User
from enrollments.models import StudentEnrollment, GroupEnrollment, RecruitmentStrategy
from courses.models import CourseGroup


class Command(PopulateCommand):
    help = 'Populate the enrollments_student_enrollment table with sample data'

    def populate(self):
        config = self.config.get('student_enrollment', {})
        self.clear_data()
        self.make_student_enrollments(config.get('ratio', 1), config.get('errors_in_row_limit'))
        self.accept_enrollments()
    
    def make_student_enrollments(self, ratio, errors_in_row_limit):
        students = User.objects.filter(groups__name='Students')
        group_enrollments = GroupEnrollment.objects.all()

        errors = 0
        counter = 0
        spots = int(self.get_available_spots(group_enrollments) * ratio)

        while counter <= spots and errors < errors_in_row_limit:
            group_enrollment = random.choice(group_enrollments)
            try:
                StudentEnrollment.objects.create(
                    student=random.choice(students),
                    group_enrollment = group_enrollment
                )
            except ValidationError as e:
                errors += 1
                if 'There are no available spots in this class.' in str(e):
                    group_enrollments = group_enrollments.exclude(id=group_enrollment.id)
            else:
                errors = 0
                counter += 1
                self.stdout.write(self.style.SUCCESS(f'\rProgress {counter}/{spots} '), ending='')
        
        self.stdout.write()
        self.stdout.write(self.style.SUCCESS(f'Successfully populated enrollments_student_enrollment. '))
    
    def accept_enrollments(self):
        manual_recruitment = RecruitmentStrategy.objects.get(id=1)
        group_enrollments = GroupEnrollment.objects.filter(recruitment_strategy=manual_recruitment)
        for group_enrollment in group_enrollments:
            while True:
                try:
                    random.choice(group_enrollment.student_applications.all()).accept()
                except Exception:
                    break
    
    def clear_data(self):
        StudentEnrollment.objects.all().delete()
        for course_group in CourseGroup.objects.all():
            course_group.students.clear()
    
    @staticmethod
    def get_available_spots(group_enrollments):
        return group_enrollments.aggregate(total_max_students=Sum('max_students'))['total_max_students']
