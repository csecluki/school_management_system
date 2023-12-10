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
from .serializers import LessonUnitSerializer, PeriodSerializer, GroupTimeTableSerializer


class LessonUnitViewSet(viewsets.ModelViewSet):
    queryset = LessonUnit.objects.all()
    serializer_class = LessonUnitSerializer


class PeriodViewSet(viewsets.ModelViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer


class GroupTimeTableViewSet(viewsets.ModelViewSet):
    """
    todo: add filters and permissions
    """
    queryset = GroupTimeTable.objects.all()
    serializer_class = GroupTimeTableSerializer
    pagination_class = TimetablePageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = GroupTimeTableFilter

    @action(methods=['GET'], detail=False)
    def enrolled_courses(self, request):
        class_schedule = self.queryset.filter(course_group__in=request.user.enrolled_courses.all())
        serializer = self.get_serializer(class_schedule, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)    
    def generate_student_class_schedule(self, request):
        # todo: add javascript to template
        lesson_units = LessonUnit.objects.all()
        class_schedule = self.queryset.filter(course_group__in=request.user.enrolled_courses.all())

        html_string = render_to_string(
            'timetables/class_schedule.html',
            {'classes': class_schedule, 'lesson_units': lesson_units}
        )
        
        pdf_file = HTML(string=html_string).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf', status=status.HTTP_200_OK)
        response['Content-Disposition'] = 'filename=class_schedule.pdf'
        return response
