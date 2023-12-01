import django_filters

from .models import Room


class RoomFilter(django_filters.FilterSet):
    capacity = django_filters.RangeFilter()

    class Meta:
        model = Room
        fields = ['room_number', 'capacity', ]
