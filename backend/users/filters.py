import django_filters

from .models import User, Profile


class UserFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['email', ]


class ProfileFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', ]
