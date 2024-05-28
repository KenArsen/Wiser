from rest_framework import serializers

from apps.order.models import Order

from .common_serializer import PointSerializer


class MyBidListSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        ref_name = "MyBidList"


class MyBidDetailSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        ref_name = "MyBidDetail"


class MyBidHistorySerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        ref_name = "MyBidHistory"
