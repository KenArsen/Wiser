from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response

from apps.common.paginations import LargeResultsSetPagination
from apps.common.permissions import HasAccessToLoadBoardPanel
from apps.order.api.v1.serializers.common import RefuseSerializer
from apps.order.api.v1.serializers.order import (
    OrderCreateSerializer,
    OrderDetailSerializer,
    OrderListSerializer,
    OrderUpdateSerializer,
)
from apps.order.models import Order
from apps.order.repositories.implementations.order import OrderRepository
from apps.order.services.implementations.order import (
    CreateOrderService,
    DeleteOrderService,
    RefuseOrderService,
    UpdateOrderService,
)


class BaseOrderView(GenericAPIView):
    queryset = OrderRepository().none()
    permission_classes = (HasAccessToLoadBoardPanel,)
    pagination_class = LargeResultsSetPagination

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.order_repository = OrderRepository()
        self.create_order_service = CreateOrderService(repository=self.order_repository)
        self.update_order_service = UpdateOrderService(repository=self.order_repository)
        self.delete_order_service = DeleteOrderService(repository=self.order_repository)
        self.refuse_order_service = RefuseOrderService(repository=self.order_repository)

    def get_object(self):
        try:
            return self.order_repository.retrieve_order(pk=self.kwargs["pk"])
        except Order.DoesNotExist:
            raise ValidationError({"detail": "Order not found"})


class OrderListAPI(BaseOrderView, ListAPIView):
    serializer_class = OrderListSerializer

    def get_queryset(self):
        return self.order_repository.list_orders()


class OrderCreateAPI(BaseOrderView, CreateAPIView):
    serializer_class = OrderCreateSerializer

    def perform_create(self, serializer):
        print()
        print(serializer.validated_data)
        print(self.request.user)
        print()
        serializer.instance = self.create_order_service.create_order(
            data=serializer.validated_data, user=self.request.user
        )


class OrderDetailAPI(BaseOrderView, RetrieveAPIView):
    serializer_class = OrderDetailSerializer


class OrderUpdateAPI(BaseOrderView, UpdateAPIView):
    serializer_class = OrderUpdateSerializer

    def perform_update(self, serializer):
        serializer.instance = self.update_order_service.update_order(
            order=self.get_object(), data=serializer.validated_data
        )


class OrderDeleteAPI(BaseOrderView, DestroyAPIView):

    def perform_destroy(self, serializer):
        self.delete_order_service.delete_order(order=self.get_object())


class OrderRefuseAPI(BaseOrderView):
    serializer_class = RefuseSerializer

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        if not order:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        self.refuse_order_service.refuse_order(order=order)
        return Response({"detail": "The order has been moved to HISTORY"}, status=status.HTTP_200_OK)
