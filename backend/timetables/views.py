from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import LessonUnit, Period, GroupTimeTable
from .serializers import LessonUnitSerializer, PeriodSerializer, GroupTimeTableSerializer


class LessonUnitViewSet(viewsets.ModelViewSet):
    queryset = LessonUnit.objects.all()
    serializer_class = LessonUnitSerializer


class PeriodViewSet(viewsets.ModelViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer


class GroupTimeTableViewSet(viewsets.ModelViewSet):
    queryset = GroupTimeTable.objects.all()
    serializer_class = GroupTimeTableSerializer
