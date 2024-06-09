import abc
from typing import Dict

from apps.order.models import Order


class ICreateOrderService(abc.ABC):
    @abc.abstractmethod
    def create_order(self, data: Dict[str, any], user: any) -> Order:
        """Create a new order."""
        pass


class IUpdateOrderService(abc.ABC):
    @abc.abstractmethod
    def update_order(self, order: Order, data: Dict[str, any]) -> Order:
        """Update an existing order."""
        pass


class IDeleteOrderService(abc.ABC):
    @abc.abstractmethod
    def delete_order(self, order: Order) -> None:
        """Delete an existing order."""
        pass


class IRefuseOrderService(abc.ABC):
    @abc.abstractmethod
    def refuse_order(self, order: Order) -> None:
        """Refuse an existing order."""
        pass


class IAssignOrderService(abc.ABC):
    @abc.abstractmethod
    def assign_order(self, data: Dict[str, any]) -> None:
        """Assign an order to a user."""
        pass
