from django.db import models

from users.models import User
from courses.models import Course, CourseGroup


class EndNote(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_end_notes')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_notes')
    date_time = models.DateTimeField(auto_now=True)

    class Meta:
        default_permissions = ()


class Note(models.Model):

    course_group = models.ForeignKey(CourseGroup, on_delete=models.CASCADE, related_name='course_group_notes')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_notes')
    date_time = models.DateTimeField(auto_now=True)

    class Meta:
        default_permissions = ()
