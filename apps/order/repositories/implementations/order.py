from typing import Any

from django.db.models import Q, QuerySet
from rest_framework.exceptions import ValidationError

from apps.order.models import Order

from ..interfaces.order import (
    ILoadBoardRepository,
    IMyBidRepository,
    IMyLoadRepository,
    IOrderRepository,
)


class OrderRepository(IOrderRepository):
    def list_orders(self) -> list[Order]:
        return Order.objects.all()

    def retrieve_order(self, pk: int) -> Order:
        try:
            return Order.objects.get(id=pk)
        except Order.DoesNotExist:
            raise ValidationError({"detail": "Order not found"})

    def create_order(self, data: dict, user: Any) -> Order:
        data["user"] = user
        return Order.objects.create(**data)

    def update_order(self, order: Order, data: dict) -> Order:
        for key, value in data.items():
            setattr(order, key, value)
        order.save()
        return order

    def delete_order(self, order: Order) -> None:
        if order.user:
            order.status = "EXPIRED"
            order.save(update_fields=["status", "updated_at"])
        else:
            order.delete()

    def refuse_order(self, order: Order) -> None:
        order.status = "REFUSED"
        order.save(update_fields=["status", "updated_at"])

    def none(self) -> QuerySet[Order]:
        return Order.objects.none()


class LoadBoardRepository(ILoadBoardRepository):
    def list_orders(self) -> list[Order]:
        return Order.objects.filter(status="PENDING")

    def retrieve_order(self, pk: int) -> Order:
        try:
            return Order.objects.get(id=pk, status="PENDING")
        except Order.DoesNotExist:
            raise ValidationError({"detail": "Order not found"})

    def none(self) -> QuerySet[Order]:
        return Order.objects.none()


class MyBidRepository(IMyBidRepository):
    def get_history_orders(self) -> list[Order]:
        return Order.objects.filter(
            Q(status="REFUSED") | Q(status="ACTIVE") | Q(status="CHECKOUT") | Q(status="COMPLETED")
        )

    def list_orders(self) -> list[Order]:
        return Order.objects.filter(status="AWAITING_BID")

    def retrieve_order(self, pk: int) -> Order:
        try:
            return Order.objects.get(id=pk, status="AWAITING_BID")
        except Order.DoesNotExist:
            raise ValidationError({"detail": "Order not found"})

    def none(self) -> QuerySet[Order]:
        return Order.objects.none()


class MyLoadRepository(IMyLoadRepository):
    def retrieve_order(self, pk: int) -> Order:
        try:
            return Order.objects.get(
                Q(status="COMPLETED")
                | Q(status="CHECKOUT")
                | Q(status="ACTIVE")
                | Q(status="REFUSED", assign__isnull=False),
                id=pk,
            )
        except Order.DoesNotExist:
            raise ValidationError({"detail": "Order not found"})

    def get_order_for_update_substatus(self, pk: int) -> Order:
        return Order.objects.get(
            Q(status="COMPLETED") | Q(status="CHECKOUT") | Q(status="ACTIVE"),
            id=pk,
        )

    def get_history_orders(self) -> list[Order]:
        return Order.objects.filter(Q(status="REFUSED", assign__isnull=False) | Q(status="COMPLETED"))

    def get_checkout_orders(self) -> list[Order]:
        return Order.objects.filter(status="CHECKOUT")

    def get_completed_orders(self) -> list[Order]:
        return Order.objects.filter(status="COMPLETED")

    def list_orders(self) -> list[Order]:
        return Order.objects.filter(status="ACTIVE")

    def none(self) -> QuerySet[Order]:
        return Order.objects.none()
