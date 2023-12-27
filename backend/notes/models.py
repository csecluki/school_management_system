from django.db import models
from rest_framework.exceptions import ValidationError

from users.models import User
from courses.models import Course, CourseGroup


class EndNote(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_end_notes')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_end_notes')
    date_time = models.DateTimeField(auto_now=True)

    class Meta:
        default_permissions = ()
    
    def clean(self):
        if not self.course.teacher.is_teacher:
            raise ValidationError({'error': f"User {self.course_group.teacher.id} is not a Teacher. "})
        if not self.student in self.course_group.students:
            raise ValidationError({'error': f"User {self.student.id} is not in this group. "})
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Note(models.Model):

    course_group = models.ForeignKey(CourseGroup, on_delete=models.CASCADE, related_name='course_group_notes')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_notes')
    date_time = models.DateTimeField(auto_now=True)

    class Meta:
        default_permissions = ()
    
    def clean(self):
        if not self.course_group.teacher.is_teacher:
            raise ValidationError({'error': f"User {self.course_group.teacher.id} is not a Teacher. "})
        if not self.student in self.course_group.students.all():
            return ValidationError({'error': f"User {self.student.id} is not in this group. "})
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
