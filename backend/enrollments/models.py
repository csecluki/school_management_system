from django.db import models
from django.core.exceptions import ValidationError

from users.models import User
from courses.models import CourseGroup


class RecruitmentStrategy(models.Model):

    STRATEGY_CHOICES = [
        (0, 'First in first served'),
        (1, 'Manual'),
    ]

    id = models.PositiveSmallIntegerField(choices=STRATEGY_CHOICES, primary_key=True)
    is_auto_triggered = models.BooleanField()

    class Meta:
        default_permissions = ()

    def execute_acceptance_logic(self, student_enrollment: 'StudentEnrollment'):
        if self.id == 0 and student_enrollment.status == 0:
            self.first_in_first_served(student_enrollment)
        elif self.id == 1 and student_enrollment.status == 1:
            self.manual(student_enrollment)
    
    def first_in_first_served(self, student_enrollment: 'StudentEnrollment'):
        student_enrollment.accept()
        student_enrollment.group_enrollment.course_group.add_student(student_enrollment.student)
    
    def manual(self, student_enrollment: 'StudentEnrollment'):
        student_enrollment.group_enrollment.course_group.add_student(student_enrollment.student)
        if student_enrollment.group_enrollment.limit_reached:
            student_enrollment.group_enrollment.reject_all_unaccepted_student_enrollments()


class GroupEnrollment(models.Model):
    
    course_group = models.ForeignKey(CourseGroup, on_delete=models.CASCADE, related_name='enrollments')
    max_students = models.PositiveSmallIntegerField()
    recruitment_strategy = models.ForeignKey(RecruitmentStrategy, on_delete=models.CASCADE, null=True, blank=True)

    @property
    def limit_reached(self) -> bool:
        return self.course_group.students.count() >= self.max_students
    
    @property
    def applications_count(self) -> int:
        return self.student_applications.count()

    class Meta:
        default_permissions = ()
    
    def clean(self):
        if GroupEnrollment.objects.filter(
            course_group=self.course_group
        ).exists():
            raise ValidationError({'error': 'Enrollment for this course_group already exists. '})
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def trigger_recruitment_strategy(self, student_enrollment: 'StudentEnrollment'):
        return self.recruitment_strategy.execute_acceptance_logic(student_enrollment)
    
    def resolve(self):
        return self.recruitment_strategy.execute_acceptance_logic(final=True)
    
    def reject_all_unaccepted_student_enrollments(self):
        self.student_applications.filter(status=0).update(status=2)


class StudentEnrollment(models.Model):
    
    STATUS_CHOICES = [
        (0, 'pending'),
        (1, 'accepted'),
        (2, 'rejected'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    group_enrollment = models.ForeignKey(GroupEnrollment, on_delete=models.CASCADE, related_name='student_applications')
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        default_permissions = ()
    
    def clean(self):
        if not self.student.groups.filter(name="Students").exists():
            raise ValidationError({'error': 'Chosen user is not a student. '})
        
        if self.group_enrollment.course_group.students.filter(id=self.student.id).exists():
            raise ValidationError({'error': "Student already in class. "})
        
        existing_groups = CourseGroup.objects.filter(
            students=self.student,
            course__level=self.group_enrollment.course_group.course.level,
            course__subject=self.group_enrollment.course_group.course.subject
        )
        if existing_groups.exists():
            raise ValidationError({'error': 'Student is already in a group for the same level and subject. '})
        
        if self.group_enrollment.limit_reached:
            raise ValidationError({'error': "There are no available spots in this class. "})
        
        last_request = self.get_last_student_enrollment_for_group(self)
        if self.status == 0 and last_request:
            raise ValidationError({'error': f"Application already sent, status: {last_request.get_status_display()}. "})
    
    def save(self, *args, **kwargs): # todo: add parameter not to trigger_recruitment_strategy
        self.clean()
        if not self.pk:
            self.status = 0
        super().save(*args, **kwargs)
        if self.group_enrollment.recruitment_strategy.is_auto_triggered:
            self.group_enrollment.trigger_recruitment_strategy(self)
    
    def accept(self):
        self.status = 1
        self.save()
    
    def reject(self):
        self.status = 2
        self.save()
    
    def get_last_student_enrollment_for_group(self, instance: 'StudentEnrollment'):
        return StudentEnrollment.objects.filter(
            student=instance.student,
            group_enrollment=instance.group_enrollment
        ).order_by('-update_date').first()
