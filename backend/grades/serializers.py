from rest_framework import serializers

from .models import Grade, EndGrade


class GradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields = '__all__'
        read_only_fields = ('id', )


class EndGradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EndGrade
        fields = '__all__'
        read_only_fields = ('id', )
