from rest_framework import serializers

from .models import Note, EndNote


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ('id', )


class EndNoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = EndNote
        fields = '__all__'
        read_only_fields = ('id', )
