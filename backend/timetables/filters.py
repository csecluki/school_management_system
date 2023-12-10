import django_filters

from .models import GroupTimeTable


class GroupTimeTableFilter(django_filters.FilterSet):

    class Meta:
        model = GroupTimeTable
        fields = ['day_of_week', 'lesson_unit', 'room', ]
