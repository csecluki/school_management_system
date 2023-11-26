from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Subject, Course, CourseGroup
from .pagination import CoursePageNumberPagination
from .serializers import SubjectSerializer, CourseSerializer, CourseGroupSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    pagination_class = CoursePageNumberPagination


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseGroupViewSet(viewsets.ModelViewSet):
    queryset = CourseGroup.objects.all()
    serializer_class = CourseGroupSerializer
    pagination_class = CoursePageNumberPagination

    @action(methods=['GET'], detail=False)
    def enrolled_courses(self, request):
        serializer = self.get_serializer(request.user.enrolled_courses.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def conducted_courses(self, request):
        serializer = self.get_serializer(request.user.conducted_courses.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
