from rest_framework import serializers


class LetterSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {"id": instance.id, "comment": instance.comment}
