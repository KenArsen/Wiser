from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError

from apps.common.enums import SubStatus
from apps.order.models import MyLoadStatus

from .order_service import OrderService


class MyBidService(OrderService):
    def _get_order(self, data):
        order_id = data.get("order", None)
        if order_id is None:
            raise ValidationError({"detail": "order field is required."})
        order = self.get_order(pk=order_id)
        return order

    @transaction.atomic
    def assign(self, data):
        order = self._get_order(data=data)
        if order.status != "ACTIVE":
            order.status = "ACTIVE"
            order.save(update_fields=["status"])

            try:
                MyLoadStatus.objects.create(
                    order=order,
                    current_status=SubStatus.POINT_A.value,
                    next_status=SubStatus.UPLOADED.value,
                )
            except IntegrityError:
                raise ValidationError({"detail": "Order already assigned."})

            broker_price = data.get("broker_price")
            driver_price = data.get("driver_price")

            if broker_price is not None:
                order.letter.broker_price = broker_price
                order.letter.save(update_fields=["broker_price"])

            if driver_price is not None:
                order.letter.driver_price = driver_price
                order.letter.save(update_fields=["driver_price"])

            serializer = self.serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return {"detail": "The order has been moved to My Loads"}
        else:
            raise ValidationError({"detail": "Order is already assigned."})