from django.db.models import Q
from django.db.models.query import QuerySet
from rest_framework.exceptions import ValidationError

from apps.order.models import Order
from apps.order.repositories.interfaces.order import (
    IloadBoardRepository,
    IMyBidRepository,
    IMyLoadRepository,
    IOrderRepository,
)


class OrderRepository(IOrderRepository):
    def get_by_id(self, pk) -> Order:
        try:
            return Order.objects.get(id=pk)
        except Order.DoesNotExist:
            raise ValidationError({"detail": "Order not found"})

    def create(self, data, user) -> Order:
        data["user"] = user
        return Order.objects.create(**data)

    def update(self, order, data) -> Order:
        for key, value in data.items():
            setattr(order, key, value)
        order.save()
        return order

    def delete(self, order) -> None:
        if order.user:
            order.status = "EXPIRED"
            order.save(update_fields=["status", "updated_at"])
        else:
            order.delete()

    def refuse(self, order) -> None:
        order.status = "REFUSED"
        order.save(update_fields=["status", "updated_at"])

    def none(self) -> QuerySet[Order]:
        return Order.objects.none()

    def list(self) -> list[Order]:
        return Order.objects.filter().order_by("-updated_at", "-id")


class LoadBoardRepository(IloadBoardRepository):
    def list(self) -> list[Order]:
        return Order.objects.filter(status="PENDING")

    def get_by_id(self, pk) -> Order:
        try:
            return Order.objects.get(id=pk, status="PENDING")
        except Order.DoesNotExist:
            raise ValidationError({"detail": "Order not found"})

    def none(self) -> QuerySet[Order]:
        return Order.objects.none()


class MyBidRepository(IMyBidRepository):
    def history_list(self) -> list[Order]:
        return Order.objects.filter(
            Q(status="REFUSED") | Q(status="ACTIVE") | Q(status="CHECKOUT") | Q(status="COMPLETED")
        )

    def list(self) -> list[Order]:
        return Order.objects.filter(status="AWAITING_BID")

    def get_by_id(self, pk) -> Order:
        try:
            return Order.objects.get(id=pk, status="AWAITING_BID")
        except Order.DoesNotExist:
            raise ValidationError({"detail": "Order not found"})

    def none(self) -> QuerySet[Order]:
        return Order.objects.none()


class MyLoadRepository(IMyLoadRepository):
    def history_list(self) -> list[Order]:
        return Order.objects.filter(Q(status="REFUSED", assign__isnull=False) | Q(status="COMPLETED"))

    def checkout_list(self) -> list[Order]:
        return Order.objects.filter(status="CHECKOUT")

    def completed_list(self) -> list[Order]:
        return Order.objects.filter(status="COMPLETED")

    def list(self) -> list[Order]:
        return Order.objects.filter(status="ACTIVE")

    def get_by_id(self, pk) -> Order:
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

    def get_by_id_for_my_load_status(self, pk) -> Order:
        try:
            return Order.objects.get(
                Q(status="COMPLETED") | Q(status="CHECKOUT") | Q(status="ACTIVE"),
                id=pk,
            )
        except Order.DoesNotExist:
            raise ValidationError({"detail": "Order not found"})

    def none(self) -> QuerySet[Order]:
        return Order.objects.none()
