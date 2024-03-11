from rest_framework import serializers

from apps.letter.models import Letter


class LetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letter
        fields = ('id', 'comment')
