from rest_framework import serializers

from .models import RecruitmentStrategy, GroupEnrollment, StudentEnrollment


class RecruitmentStrategySerializer(serializers.ModelSerializer):

    class Meta:
        model = RecruitmentStrategy
        fields = '__all__'
        read_only_fields = ('id', )


class GroupEnrollmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupEnrollment
        fields = '__all__'
        read_only_fields = ('id', )


class StudentEnrollmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentEnrollment
        fields = '__all__'
        read_only_fields = ('id', )
