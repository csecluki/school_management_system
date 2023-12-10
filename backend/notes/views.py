from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .filters import NoteFilter, EndNoteFilter
from .models import Note, EndNote
from .pagination import NotePageNumberPagination
from .permissions import NotePermission, EndNotePermission
from .serializers import NoteSerializer, EndNoteSerializer


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    pagination_class = NotePageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = NoteFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, NotePermission, ]


class EndNoteViewSet(viewsets.ModelViewSet):
    queryset = EndNote.objects.all()
    serializer_class = EndNoteSerializer
    pagination_class = NotePageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = EndNoteFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, EndNotePermission, ]
