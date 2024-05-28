from rest_framework import serializers

from apps.order.models import Order
from . import LetterSerializer

from .common_serializer import PointSerializer


class MyBidListSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'created_at', 'points', 'order_number', 'broker')
        ref_name = "MyBidDetail"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        letter = getattr(instance, 'letter', None)
        dispatcher = getattr(letter, 'dispatcher', None)

        if dispatcher:
            name = f'{dispatcher.first_name} {dispatcher.last_name}'
            representation['dispatcher'] = name
            representation['dispatcher_phone'] = dispatcher.phone_number
        else:
            representation['dispatcher'] = None
            representation['dispatcher_phone'] = None

        price = getattr(instance, 'price', None)

        if price:
            representation['broker_price'] = price.broker_price
        else:
            representation['broker_price'] = None


class MyBidDetailSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True, read_only=True)
    letter = LetterSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        ref_name = "MyBidDetail"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        letter = getattr(instance, 'letter', None)
        dispatcher = getattr(letter, 'dispatcher', None)
        price = getattr(instance, 'price', None)

        if price:
            representation['broker_price'] = price.broker_price
            representation['driver_price'] = price.driver_price
        else:
            representation['broker_price'] = None
            representation['driver_price'] = None

        if dispatcher:
            name = f'{dispatcher.first_name} {dispatcher.last_name}'
            representation['dispatcher'] = name
            representation['dispatcher_phone'] = dispatcher.phone_number
            representation['dispatcher_email'] = dispatcher.email
        else:
            representation['dispatcher'] = None
            representation['dispatcher_phone'] = None
            representation['dispatcher_email'] = None

        return representation


class MyBidHistorySerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        ref_name = "MyBidHistory"
