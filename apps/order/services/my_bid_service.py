from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError

from apps.common.enums import SubStatus
from apps.order.api.v1.serializers import PriceSerializer
from apps.order.models import MyLoadStatus

from .order_service import OrderService


class MyBidService(OrderService):
    def _get_order(self, data):
        order_id = data.get("order_id", None)
        if order_id is None:
            raise ValidationError({"detail": "order_id field is required."})
        order = self.repository.get_order(pk=order_id)
        return order

    @transaction.atomic
    def assign(self, data):
        order = self._get_order(data=data)
        order.status = "ACTIVE"
        order.save()

        try:
            MyLoadStatus.objects.create(
                order=order,
                current_status=SubStatus.POINT_A.value,
                next_status=SubStatus.UPLOADED.value,
            )
        except IntegrityError:
            raise ValidationError({"detail": "Order already assigned."})

        broker_price = data.pop("broker_price", None)
        driver_price = data.pop("driver_price", None)
        if broker_price is not None and driver_price is not None:
            price_data = {
                "broker_price": broker_price,
                "driver_price": driver_price,
                "order": order.id,
                "driver": order.letter.driver.id,
                "dispatcher": order.letter.dispatcher.id,
            }

            serializer = PriceSerializer(data=price_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        serializer = self.serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return {"detail": "The order has been moved to My Loads"}
