from django.db import transaction
from rest_framework import serializers

from .models import RecruitmentStrategy, GroupEnrollment, StudentEnrollment, Enrollment, EnrollmentPhase


class RecruitmentStrategySerializer(serializers.ModelSerializer):

    class Meta:
        model = RecruitmentStrategy
        fields = '__all__'
        read_only_fields = ('id', )


class EnrollmentPhaseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EnrollmentPhase
        fields = '__all__'
        read_only_fields = ('id', 'enrollment', 'stage')


class EnrollmentPhaseUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EnrollmentPhase
        fields = ('start_date', 'application_deadline', 'decision_deadline')


class EnrollmentSerializer(serializers.ModelSerializer):
    phases = EnrollmentPhaseSerializer(many=True, required=False)

    class Meta:
        model = Enrollment
        fields = '__all__'
        read_only_fields = ('id', )

    def create(self, validated_data):
        phases_data = validated_data.pop('phases')
        with transaction.atomic():
            enrollment = Enrollment.objects.create(**validated_data)
            for phase_data in phases_data:
                EnrollmentPhase.objects.create(enrollment=enrollment, **phase_data)
            return enrollment


class GroupEnrollmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupEnrollment
        fields = '__all__'
        read_only_fields = ('id', )


class StudentEnrollmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentEnrollment
        fields = '__all__'
        read_only_fields = ('id', 'joined', )
