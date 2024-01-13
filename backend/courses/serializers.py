from rest_framework import serializers

from .models import Subject, Course, CourseGroup


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = '__all__'
        read_only_fields = ('id', )


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ('id', )


class CourseGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseGroup
        fields = '__all__'
        read_only_fields = ('id', 'group_number', 'students', )
