from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import GradeFilter, EndGradeFilter
from .models import Grade, EndGrade
from .pagination import GradePageNumberPagination
from .permissions import GradePermission, EndGradePermission
from .serializers import GradeSerializer, EndGradeSerializer

from courses.models import CourseGroup


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    pagination_class = GradePageNumberPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = GradeFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, GradePermission, ]

    def create(self, request, *args, **kwargs):
        course_group = CourseGroup.objects.get(id=request.data.get('course_group', None))
        if not GradePermission().has_permission_for_create_destroy(request, course_group):
            raise PermissionDenied("You don't have permission to create a grade for this course group.")
        return super().create(request, *args, **kwargs)
    
    @action(methods=['GET'], detail=False)
    def student_grades(self, request):
        queryset = self.filter_queryset(request.user.student_grades.all())
        serializer = self.get_serializer(self.paginate_queryset(queryset), many=True)
        return self.paginator.get_paginated_response(serializer.data)


class EndGradeViewSet(viewsets.ModelViewSet):
    queryset = EndGrade.objects.all()
    serializer_class = EndGradeSerializer
    pagination_class = GradePageNumberPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = EndGradeFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, EndGradePermission, ]
