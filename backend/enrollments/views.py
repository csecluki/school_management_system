from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import RecruitmentStrategy, GroupEnrollment, StudentEnrollment
from .serializers import RecruitmentStrategySerializer, GroupEnrollmentSerializer, StudentEnrollmentSerializer


class RecruitmentStrategyViewSet(viewsets.ModelViewSet):
    queryset = RecruitmentStrategy.objects.all()
    serializer_class = RecruitmentStrategySerializer


class GroupEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = GroupEnrollment.objects.all()
    serializer_class = GroupEnrollmentSerializer


class StudentEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = StudentEnrollment.objects.all()
    serializer_class = StudentEnrollmentSerializer
