from rest_framework import serializers

from .models import LessonUnit, Period, GroupTimeTable


class LessonUnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = LessonUnit
        fields = '__all__'
        read_only_fields = ('id', )


class PeriodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Period
        fields = '__all__'
        read_only_fields = ('id', )


class GroupTimeTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupTimeTable
        fields = '__all__'
        read_only_fields = ('id', )
