from rest_framework.exceptions import ValidationError

from apps.order.repositories import OrderRepository


class OrderService:
    repository = OrderRepository

    def __init__(self, serializer):
        self.serializer = serializer

    def get_order(self, pk):
        return self.repository.get_order(pk=pk)

    def get_orders_by_status(self, status_):
        return self.repository.get_orders_by_status(status_=status_)

    def get_orders(self):
        return self.repository.get_orders()

    def create_order(self, data):
        serializer = self.serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            raise ValidationError(serializer.errors)

    def update_order(self, instance, data, partial=False):
        serializer = self.serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def delete_order(self, instance):
        if instance.user:
            instance.order_status = "EXPIRED"
            instance.save()
            return {"detail": "This order has been marked as inactive."}
        else:
            instance.delete()
            return {"detail": "Order deleted successfully."}
