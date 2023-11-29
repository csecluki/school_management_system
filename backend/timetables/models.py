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

    @property
    def teacher(self):
        return self.course_group.course.teacher

    class Meta:
        default_permissions = ()

    def clean(self):
        existing_groups = GroupTimeTable.objects.filter(
            day_of_week=self.day_of_week,
            lesson_unit=self.lesson_unit,
        )
        
        if self.room:
            room_busy = existing_groups.filter(
                room=self.room
            ).exclude(pk=self.pk)

            if room_busy.exists():
                raise ValidationError({'error': "Room is busy at this time. "})
        
        teacher_existing_groups = existing_groups.filter(
            course_group__course__teacher=self.course_group.course.teacher,
            course_group__period=self.course_group.period,
        ).exclude(pk=self.pk)
        if teacher_existing_groups.exists():
            return ValidationError({'error': "Teacher has lesson at this time. "})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
