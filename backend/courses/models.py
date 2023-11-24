from django.db import models
from django.core.exceptions import ValidationError

from users.models import User


class Subject(models.Model):

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        default_permissions = ()
        permissions = []

    def __str__(self):
        return self.name


class Course(models.Model):

    LEVEL_CHOICES = [
        (1, 'I'),
        (2, 'II'),
        (3, 'III'),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conducted_courses')
    description = models.TextField(null=True, blank=True)

    @property
    def name(self):
        return f"{self.subject} {self.get_level_display()} {self.teacher.profile.last_name or self.teacher.id}"

    class Meta:
        default_permissions = ()

    def __str__(self):
        return self.name
    
    def clean(self):
        if not self.teacher.groups.filter(name="Teachers").exists():
            raise ValidationError({'error': 'Chosen user is not a teacher. '})
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
