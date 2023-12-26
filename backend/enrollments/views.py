from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .filters import GroupEnrollmentFilter
from .models import RecruitmentStrategy, GroupEnrollment, StudentEnrollment
from .serializers import RecruitmentStrategySerializer, GroupEnrollmentSerializer, StudentEnrollmentSerializer
from .pagination import EnrollmentPageNumberPagination
from .permissions import GroupEnrollmentPermission, StudentEnrollmentPermission


class RecruitmentStrategyViewSet(viewsets.ModelViewSet):
    queryset = RecruitmentStrategy.objects.all()
    serializer_class = RecruitmentStrategySerializer


class GroupEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = GroupEnrollment.objects.all()
    serializer_class = GroupEnrollmentSerializer
    pagination_class = EnrollmentPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = GroupEnrollmentFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, GroupEnrollmentPermission, ]


class StudentEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = StudentEnrollment.objects.all()
    serializer_class = StudentEnrollmentSerializer
    pagination_class = EnrollmentPageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentEnrollment
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, StudentEnrollmentPermission, ]
