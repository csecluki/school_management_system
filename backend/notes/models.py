from django.db import models
from rest_framework.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User
from courses.models import Course, CourseGroup


def divisible_by_0_5(value):
    if value % 0.5 != 0:
        return value
    else:
        raise ValidationError({'error': f'Value {value} is not divisible by 0.5. '})


def not_1_5(value):
    if value != 1.5:
        return value
    else:
        raise ValidationError({'error': f"Note shouldn't be 1.5. "})


class EndNote(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_end_notes')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_end_notes')
    value = models.FloatField(
        validators=[
            divisible_by_0_5,
            not_1_5,
            MinValueValidator(limit_value=1.0),
            MaxValueValidator(limit_value=6.0),
        ]
    )
    date_time = models.DateTimeField(auto_now=True)

    class Meta:
        default_permissions = ()
        unique_together = ['course', 'student']
    
    def clean(self):
        if not self.course.teacher.is_teacher:
            raise ValidationError({'error': f"User {self.course_group.teacher.id} is not a Teacher. "})
        if not CourseGroup.objects.filter(course=self.course, students=self.student).exists():
            raise ValidationError({'error': f"User {self.student.id} is not added to any group for this course. "})
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Note(models.Model):

    course_group = models.ForeignKey(CourseGroup, on_delete=models.CASCADE, related_name='course_group_notes')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_notes')
    value = models.FloatField(
        validators=[
            divisible_by_0_5,
            not_1_5,
            MinValueValidator(limit_value=1.0),
            MaxValueValidator(limit_value=6.0),
        ]
    )
    date_time = models.DateTimeField(auto_now=True)

    class Meta:
        default_permissions = ()
    
    def clean(self):
        if not self.course_group.teacher.is_teacher:
            raise ValidationError({'error': f"User {self.course_group.teacher.id} is not a Teacher. "})
        if not self.student in self.course_group.students.all():
            raise ValidationError({'error': f"User {self.student.id} is not in this group. "})
        if not 1 <= self.value <= 6:
            raise ValidationError({'error': f"Note value should be between 1 and 6. "})
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
