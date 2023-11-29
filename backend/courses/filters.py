import django_filters

from .models import Subject, Course, CourseGroup

from timetables.models import Period


class SubjectFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Subject
        fields = ['name', ]


class CourseFilter(django_filters.FilterSet):
    subject__name = django_filters.CharFilter(
        field_name='subject__name',
        lookup_expr='icontains'
    )
    teacher__profile__last_name = django_filters.CharFilter(
        field_name='teacher__profile__last_name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Course
        fields = ['subject', 'subject__name', 'level', 'teacher', 'teacher__profile__last_name', ]


class CourseGroupFilter(django_filters.FilterSet):
    period = django_filters.NumberFilter(
        method='filter_by_period',
        label='Period'
    )

    class Meta:
        model = CourseGroup
        fields = ['course', 'period', ]
    
    def filter_by_period(self, queryset, name, value):
        return queryset.filter(period=value or Period.objects.get_current_period().id)
