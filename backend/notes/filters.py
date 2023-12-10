import django_filters

from .models import Note, EndNote


class NoteFilter(django_filters.FilterSet):

    class Meta:
        model = Note


class EndNoteFilter(django_filters.FilterSet):

    class Meta:
        model = EndNote
