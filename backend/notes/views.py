from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .filters import NoteFilter, EndNoteFilter
from .models import Note, EndNote
from .pagination import NotePageNumberPagination
from .permissions import NotePermission, EndNotePermission
from .serializers import NoteSerializer, EndNoteSerializer

from courses.models import CourseGroup


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    pagination_class = NotePageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = NoteFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, NotePermission, ]

    def create(self, request, *args, **kwargs):
        course_group = CourseGroup.objects.get(id=request.data.get('course_group', None))
        if not NotePermission().has_permission_for_create(request, course_group):
            raise PermissionDenied("You don't have permission to create a note for this course group.")
        return super().create(request, *args, **kwargs)


class EndNoteViewSet(viewsets.ModelViewSet):
    queryset = EndNote.objects.all()
    serializer_class = EndNoteSerializer
    pagination_class = NotePageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = EndNoteFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, EndNotePermission, ]
