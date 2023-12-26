from django.db import models
from rest_framework.exceptions import ValidationError

from users.models import User


class Subject(models.Model):

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        default_permissions = ()
        permissions = []

    def __str__(self):
        return self.name


class Course(models.Model):
    """
    Course stores data about all possible combinations of subject & level & teacher that are available. It is
    "time-independent", so informations about is Student passed course should be related to this model
    todo:
        add is_active field - so removing teacher won't affect many tables
    """

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
        unique_together = ['teacher', 'subject', 'level']

    def __str__(self):
        return self.name
    
    def clean(self):
        if not self.teacher.groups.filter(name="Teachers").exists():
            raise ValidationError({'error': 'Chosen user is not a teacher. '})
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class CourseGroup(models.Model):
    """
    Model containing informations about group created for given period. These are actual classes conducted as
    part of the course during given period. group_number field is calculated based on CourseGroups instances
    for same Course instance (so same subject & level & teacher) that's why it shouldn't be passed during
    instance creation, because it will be overwritten.
    todo:
        When creating new CourseGroup instance all GroupTimeTables (could be many for one CourseGroup) should
        also be created
    """

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='groups')
    period = models.ForeignKey('timetables.Period', on_delete=models.CASCADE, related_name='groups')
    group_number = models.PositiveIntegerField(null=True, blank=True)
    students = models.ManyToManyField(User, related_name='enrolled_courses')

    @property
    def teacher(self):
        return self.course.teacher

    class Meta:
        default_permissions = ()
        ordering = ['id']
        unique_together = ['course', 'period', 'group_number']
    
    def clean(self):
        pass

    def save(self, *args, **kwargs):
        if not self.pk:
            self.group_number = CourseGroup.objects.filter(course=self.course, period=self.period).count() + 1

        self.clean()
        super().save(*args, **kwargs)
    
    def add_student(self, student: User):
        self.students.add(student)
