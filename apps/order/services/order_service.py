from rest_framework.exceptions import ValidationError

from apps.order.repositories import OrderRepository


class OrderService(OrderRepository):
    def __init__(self, serializer, queryset):
        super().__init__(queryset=queryset)
        self.serializer = serializer

    def update_order(self, instance, data, partial=False):
        serializer = self.serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def delete_order(self, instance):
        if instance.user:
            instance.status = "EXPIRED"
            instance.save()
            return {"detail": "This order has been marked as inactive."}
        else:
            instance.delete()
            return {"detail": "Order deleted successfully."}

    def order_refuse(self, id):
        instance = self.get_order(pk=id)
        instance.status = "REFUSED"
        instance.save()
        return {"detail": "The order has been moved to HISTORY"}
