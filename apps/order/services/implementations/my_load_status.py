from rest_framework.exceptions import ValidationError

from apps.common.enums import SubStatus
from apps.order.models import MyLoadStatus
from apps.order.repositories.interfaces.my_load_status import IMyLoadStatusRepository
from apps.order.services.interfaces.my_load_status import (
    IMyLoadNextStatusService,
    IMyLoadPreviousStatusService,
    IMyLoadStatusService,
)


class MyLoadStatusService(IMyLoadStatusService):
    def __init__(self, my_load_status_repository: IMyLoadStatusRepository):
        self._my_load_status_repository = my_load_status_repository

    def create(self, data, order) -> MyLoadStatus:
        return self._my_load_status_repository.create(data, order)


class MyLoadNextStatusService(IMyLoadNextStatusService):
    def __init__(self, repository: IMyLoadStatusRepository):
        self._repository = repository

    def next_status(self, order):
        current_status = order.my_load_status.current_status

        if current_status < SubStatus.PAID_OFF:
            return self._repository.update(order, current_status + 1)
        else:
            raise ValidationError({"detail": "Cannot update status."})


class MyLoadPreviousStatusService(IMyLoadPreviousStatusService):
    def __init__(self, repository: IMyLoadStatusRepository):
        self._repository = repository

    def previous_status(self, order):
        current_status = order.my_load_status.current_status

        if current_status > SubStatus.POINT_A:
            return self._repository.update(order, current_status - 1)
        else:
            raise ValidationError({"detail": "Cannot update status."})
