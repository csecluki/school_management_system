import django_filters

from .models import Note, EndNote


class NoteFilter(django_filters.FilterSet):

    class Meta:
        model = Note
        fields = '__all__'


class EndNoteFilter(django_filters.FilterSet):

    class Meta:
        model = EndNote
        fields = '__all__'
