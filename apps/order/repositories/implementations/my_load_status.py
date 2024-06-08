from django.db.models import QuerySet

from apps.common.enums import SubStatus
from apps.order.models import MyLoadStatus
from apps.order.repositories.interfaces.my_load_status import IMyLoadStatusRepository


class MyLoadStatusRepository(IMyLoadStatusRepository):
    def list(self) -> list[MyLoadStatus]:
        pass

    def get_by_id(self, pk) -> MyLoadStatus:
        pass

    def update(self, order, current_status) -> MyLoadStatus:
        next_status = current_status + 1
        previous_status = current_status - 1 if current_status > SubStatus.POINT_A else None

        order.my_load_status.previous_status = previous_status
        order.my_load_status.current_status = current_status
        order.my_load_status.next_status = next_status
        order.my_load_status.save()

        if current_status == SubStatus.DELIVERED:
            order.status = "CHECKOUT"
        elif current_status == SubStatus.PAID_OFF:
            order.status = "COMPLETED"
        elif current_status < SubStatus.DELIVERED and order.status != "ACTIVE":
            order.status = "ACTIVE"
        elif current_status < SubStatus.PAID_OFF and order.status != "ACTIVE":
            order.status = "CHECKOUT"

        order.save(update_fields=["status", "updated_at"])

        return order.my_load_status

    def delete(self, order):
        pass

    def none(self) -> QuerySet[MyLoadStatus]:
        pass

    def create(self, data, order) -> MyLoadStatus:
        if hasattr(order, "my_load_status"):
            order.my_load_status.delete()
        return MyLoadStatus.objects.create(
            order=order,
            current_status=SubStatus.POINT_A.value,
            next_status=SubStatus.UPLOADED.value,
        )
