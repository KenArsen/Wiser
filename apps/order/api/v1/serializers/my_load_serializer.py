from rest_framework import serializers

from apps.order.models import Order

from .common_serializer import AssignSerializer, MyLoadStatusSerializer, PointSerializer
from .letter_serializer import LetterSerializer


class MyLoadListSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        ref_name = "MyLoadList"


class MyLoadDetailSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True, read_only=True)
    my_load_status = MyLoadStatusSerializer(many=False, read_only=True)
    letter = LetterSerializer(required=False, read_only=True)
    assign = AssignSerializer(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        ref_name = "MyLoadDetail"
