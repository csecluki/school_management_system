from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from users.models import User
from timetables.models import CourseTimeTable, Period


class Enrollment(models.Model):

    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        default_permissions = ()


class CourseEnrollment(models.Model):
    
    course = models.ForeignKey(CourseTimeTable, on_delete=models.CASCADE, related_name='enrollments')
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="courses")
    max_students = models.PositiveSmallIntegerField()
    
    @property
    def is_active(self):
        return self.enrollment.start_date <= timezone.localdate() <= self.enrollment.end_date
    
    @property
    def applications(self):
        return self.student_applications.count()

    class Meta:
        default_permissions = ()


class StudentEnrollment(models.Model):
    
    STATUS_CHOICES = [
        (0, 'pending'),
        (1, 'accepted'),
        (2, 'rejected'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course_enrollment = models.ForeignKey(CourseEnrollment, on_delete=models.CASCADE, related_name='student_applications')
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0)

    class Meta:
        default_permissions = ()
    
    def clean(self):
        if not self.teacher.groups.filter(name="Students").exists():
            raise ValidationError({'error': 'Chosen user is not a student. '})
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(**args, **kwargs)
