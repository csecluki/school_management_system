import random

from django.db.models import Sum
from django.core.management.base import BaseCommand
from rest_framework.exceptions import ValidationError

from users.models import User
from enrollments.models import StudentEnrollment, GroupEnrollment, RecruitmentStrategy
from courses.models import CourseGroup


class Command(BaseCommand):
    help = 'Populate the enrollments_student_enrollment table with sample data'

    def handle(self, *args, **kwargs):
        self.clear_data()
        self.make_student_enrollments()
        self.accept_enrollments()
    
    def make_student_enrollments(self):
        students = User.objects.filter(groups__name='Students')
        group_enrollments = GroupEnrollment.objects.all()

        counter = 0
        spots = int(group_enrollments.aggregate(total_max_students=Sum('max_students'))['total_max_students'])

        while counter <= spots:
            group_enrollment = random.choice(group_enrollments)
            try:
                StudentEnrollment.objects.create(
                    student=random.choice(students),
                    group_enrollment = group_enrollment
                )
            except ValidationError as e:
                print(e)
                if 'There are no available spots in this class.' in str(e):
                    group_enrollments = group_enrollments.exclude(id=group_enrollment.id)
            else:
                counter += 1
                self.stdout.write(self.style.SUCCESS(f'\rProgress {counter}/{spots} '), ending='')

        self.stdout.write(self.style.SUCCESS(f'Successfully created StudentEnrollment instances. '))
    
    def accept_enrollments(self):
        manual_recruitment = RecruitmentStrategy.objects.get(id=1)
        group_enrollments = GroupEnrollment.objects.filter(recruitment_strategy=manual_recruitment)
        for group_enrollment in group_enrollments:
            while True:
                try:
                    random.choice(group_enrollment.student_applications.all()).accept()
                except Exception as e:
                    print(e)
                    break
    
    def clear_data(self):
        StudentEnrollment.objects.all().delete()
        for course_group in CourseGroup.objects.all():
            course_group.students.clear()
