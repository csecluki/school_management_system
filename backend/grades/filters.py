import django_filters

from .models import Grade, EndGrade


class GradeFilter(django_filters.FilterSet):

    class Meta:
        model = Grade
        fields = '__all__'


class EndGradeFilter(django_filters.FilterSet):

    class Meta:
        model = EndGrade
        fields = '__all__'
