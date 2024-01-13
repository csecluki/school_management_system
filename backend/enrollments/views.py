from django.db import transaction
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import GroupEnrollmentFilter
from .models import RecruitmentStrategy, GroupEnrollment, StudentEnrollment, Enrollment, EnrollmentPhase
from .serializers import EnrollmentPhaseUpdateSerializer, RecruitmentStrategySerializer, GroupEnrollmentSerializer, StudentEnrollmentSerializer, EnrollmentSerializer, EnrollmentPhaseSerializer
from .pagination import EnrollmentPageNumberPagination
from .permissions import GroupEnrollmentPermission, StudentEnrollmentPermission, RecruitmentStrategyPermission, EnrollmentPermission


class RecruitmentStrategyViewSet(viewsets.ModelViewSet):
    queryset = RecruitmentStrategy.objects.all()
    serializer_class = RecruitmentStrategySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, RecruitmentStrategyPermission, ]


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, EnrollmentPermission, ]

    def get_active_enrolments_queryset(self):
        return Enrollment.objects.get_active()

    def get_applicable_enrolments_queryset(self):
        return Enrollment.objects.get_applicable()

    @action(methods=['POST'], detail=True)
    def add_stage(self, request, pk=None):
        enrollment = self.get_object()
        serializer = self.get_serializer(enrollment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            phase_data = serializer.validated_data.pop('phases')
            for phase in phase_data:
                EnrollmentPhase.objects.create(enrollment=enrollment, **phase)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['GET'], detail=False)
    def active(self, request):
        serializer = self.get_serializer(self.get_active_enrolments_queryset(), many=True)        
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def applicable(self, request):
        serializer = self.get_serializer(self.get_applicable_enrolments_queryset(), many=True)        
        return Response(serializer.data, status=status.HTTP_200_OK)


class EnrollmentPhaseViewSet(viewsets.ModelViewSet):
    queryset = EnrollmentPhase.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, EnrollmentPermission, ]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update', ]:
            return EnrollmentPhaseUpdateSerializer
        return EnrollmentPhaseSerializer

    def create(self, request, *args, **kwargs):
        suggested_url = reverse('enrollment-add-stage', kwargs={'pk': request.data.get('enrollment', 'specify_enrollment_id')})
        raise MethodNotAllowed('', detail=f"POST method is not allowed on this endpoint, please use POST {suggested_url}). ")


class GroupEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = GroupEnrollment.objects.all()
    serializer_class = GroupEnrollmentSerializer
    pagination_class = EnrollmentPageNumberPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = GroupEnrollmentFilter
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, GroupEnrollmentPermission, ]

    def get_open_queryset(self):
        return GroupEnrollment.objects.get_open()

    @action(methods=['GET'], detail=False)
    def open(self, request):
        serializer = self.get_serializer(self.get_open_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=False)
    def applicable(self, request):
        open = self.get_open_queryset()
        applicable = Enrollment.objects.get_applicable()
        queryset = open.filter(enrollment__in=applicable)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentEnrollmentViewSet(viewsets.ModelViewSet):
    queryset = StudentEnrollment.objects.all()
    serializer_class = StudentEnrollmentSerializer
    pagination_class = EnrollmentPageNumberPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = StudentEnrollment
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, StudentEnrollmentPermission, ]

    @action(methods=['POST'], detail=True)
    def accept(self, request, pk=None, *args, **kwargs):
        student_enrollment = self.queryset.get(id=pk)
        self.check_object_permissions(self.request, student_enrollment)
        if not student_enrollment.manual_accept_available:
            raise ValidationError(detail="Can't perform this action. ")
        student_enrollment.accept()
        return Response(data={'status': "Success. "}, status=status.HTTP_202_ACCEPTED)

    @action(methods=['POST'], detail=True)
    def reject(self, request, pk=None):
        student_enrollment = self.queryset.get(id=pk)
        self.check_object_permissions(self.request, student_enrollment)
        if not student_enrollment.manual_accept_available:
            raise ValidationError(detail="Can't perform this action. ")
        student_enrollment.reject()
        return Response(data={'status': "Success. "}, status=status.HTTP_202_ACCEPTED)

    @action(methods=['POST'], detail=True)
    def join_group(self, request, pk=None):
        student_enrollment = self.queryset.get(id=pk)
        self.check_object_permissions(self.request, student_enrollment)
        student_enrollment.join_group()
        return Response(data={'status': "Success. "}, status=status.HTTP_202_ACCEPTED)
