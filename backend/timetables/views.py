from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from weasyprint import HTML

from .filters import GroupTimeTableFilter
from .models import LessonUnit, Period, GroupTimeTable
from .pagination import TimetablePageNumberPagination
from .permissions import GroupTimeTablePermission
from .serializers import LessonUnitSerializer, PeriodSerializer, GroupTimeTableSerializer


class LessonUnitViewSet(viewsets.ModelViewSet):
    queryset = LessonUnit.objects.all()
    serializer_class = LessonUnitSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, ]


class PeriodViewSet(viewsets.ModelViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, ]


class GroupTimeTableViewSet(viewsets.ModelViewSet):
    queryset = GroupTimeTable.objects.all()
    serializer_class = GroupTimeTableSerializer
    pagination_class = TimetablePageNumberPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = GroupTimeTableFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, GroupTimeTablePermission, ]

    @action(methods=['GET'], detail=False)
    def enrolled_groups(self, request):
        class_schedule = self.queryset.filter(course_group__in=request.user.enrolled_groups.all())
        serializer = self.get_serializer(class_schedule, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)    
    def generate_student_class_schedule(self, request):
        # todo: add javascript to template
        lesson_units = LessonUnit.objects.all()
        class_schedule = self.queryset.filter(course_group__in=request.user.enrolled_groups.all())

        html_string = render_to_string(
            'timetables/class_schedule.html',
            {'classes': class_schedule, 'lesson_units': lesson_units}
        )
        
        pdf_file = HTML(string=html_string).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf', status=status.HTTP_200_OK)
        response['Content-Disposition'] = 'filename=class_schedule.pdf'
        return response

    @action(methods=['GET'], detail=False)
    def conducted_groups(self, request):
        class_schedule = self.queryset.filter(course_group__course__teacher=request.user)
        serializer = self.get_serializer(class_schedule, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)    
    def generate_teacher_class_schedule(self, request):
        # todo: add javascript to template
        lesson_units = LessonUnit.objects.all()
        class_schedule = self.queryset.filter(course_group__course__teacher=request.user)

        html_string = render_to_string(
            'timetables/class_schedule.html',
            {'classes': class_schedule, 'lesson_units': lesson_units}
        )
        
        pdf_file = HTML(string=html_string).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf', status=status.HTTP_200_OK)
        response['Content-Disposition'] = 'filename=class_schedule.pdf'
        return response
