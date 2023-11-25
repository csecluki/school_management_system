from django.core.exceptions import ValidationError
from django.db import models

from courses.models import CourseGroup
from rooms.models import Room


class LessonUnit(models.Model):

    id = models.PositiveIntegerField(primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        default_permissions = ()

    def __str__(self):
        return f"Lesson unit {self.id}: {self.start_time} - {self.end_time}"


class Period(models.Model):

    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        default_permissions = ()

    def __str__(self):
        return f'Period {self.start_date} - {self.end_date}'


class GroupTimeTable(models.Model):

    WEEK_DAYS = [
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
    ]

    course_group = models.ForeignKey(CourseGroup, on_delete=models.CASCADE, related_name='timetables')
    day_of_week = models.PositiveSmallIntegerField(choices=WEEK_DAYS)
    lesson_unit = models.ForeignKey(LessonUnit, on_delete=models.CASCADE, related_name='scheduled_courses')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, related_name='course_room', null=True, blank=True)

    class Meta:
        default_permissions = ()

    def clean(self):
        # todo: When trying to create same instance error is raised with info "Room is busy at this time. "
        existing_classes = GroupTimeTable.objects.filter(
            period=self.course_group.period,
            day_of_week=self.day_of_week,
            lesson_unit=self.lesson_unit,
            room=self.room
        ).exclude(pk=self.pk)

        if existing_classes.exists():
            raise ValidationError({'error': "Room is busy at this time. "})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
