from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import SubjectFilter, CourseFilter, CourseGroupFilter
from .models import Subject, Course, CourseGroup
from .pagination import CoursePageNumberPagination
from .serializers import SubjectSerializer, CourseSerializer, CourseGroupSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    pagination_class = CoursePageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubjectFilter


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseFilter


class CourseGroupViewSet(viewsets.ModelViewSet):
    queryset = CourseGroup.objects.all()
    serializer_class = CourseGroupSerializer
    pagination_class = CoursePageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CourseGroupFilter

    @action(methods=['GET'], detail=False)
    def enrolled_courses(self, request):
        serializer = self.get_serializer(request.user.enrolled_courses.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def conducted_courses(self, request):
        serializer = self.get_serializer(request.user.conducted_courses.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
