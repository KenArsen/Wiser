from rest_framework import serializers

from apps.order.models import Order


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        ref_name = "OrderList"


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        ref_name = "OrderDetail"


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = (
            "created_at",
            "updated_at",
            "status",
            "id",
        )
        ref_name = "OrderCreate"

    def create(self, validated_data):
        instance = Order(**validated_data)
        instance.full_clean()
        instance.save()
        return instance


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = (
            "created_at",
            "updated_at",
            "status",
        )
        ref_name = "OrderUpdate"

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.full_clean()
        instance.save()
        return instance
