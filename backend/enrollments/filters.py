import django_filters

from .models import GroupEnrollment, StudentEnrollment


class GroupEnrollmentFilter(django_filters.FilterSet):

    class Meta:
        model = GroupEnrollment
        fields = ['course_group', ]


class StudentEnrollmentFilter(django_filters.FilterSet):

    class Meta:
        model = StudentEnrollment
        fields = ['status', ]
