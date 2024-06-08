from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from apps.common.paginations import LargeResultsSetPagination
from apps.common.permissions import HasAccessToLoadBoardPanel
from apps.order.api.v1.serializers.common import RefuseSerializer
from apps.order.api.v1.serializers.order import (
    OrderCreateSerializer,
    OrderDetailSerializer,
    OrderListSerializer,
    OrderUpdateSerializer,
)
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


class OrderListAPI(BaseOrderView, ListAPIView):
    serializer_class = OrderListSerializer

    def get_queryset(self):
        return OrderRepository().list()


class OrderCreateAPI(BaseOrderView, CreateAPIView):
    serializer_class = OrderCreateSerializer

    def perform_create(self, serializer):
        service = CreateOrderService(order_repository=OrderRepository())
        serializer.instance = service.create(data=serializer.validated_data, user=self.request.user)


class OrderDetailAPI(BaseOrderView, RetrieveAPIView):
    serializer_class = OrderDetailSerializer

    def get_object(self):
        return OrderRepository().get_by_id(pk=self.kwargs["pk"])


class OrderUpdateAPI(BaseOrderView, UpdateAPIView):
    serializer_class = OrderUpdateSerializer

    def get_object(self):
        return OrderRepository().get_by_id(pk=self.kwargs["pk"])

    def perform_update(self, serializer):
        service = UpdateOrderService(order_repository=OrderRepository())
        serializer.instance = service.update(order=self.get_object(), data=serializer.validated_data)


class OrderDeleteAPI(BaseOrderView, DestroyAPIView):
    def get_object(self):
        return OrderRepository().get_by_id(pk=self.kwargs["pk"])

    def perform_destroy(self, serializer):
        service = DeleteOrderService(order_repository=OrderRepository())
        service.delete(order=self.get_object())


class OrderRefuseAPI(BaseOrderView):
    serializer_class = RefuseSerializer

    def get_object(self):
        return OrderRepository().get_by_id(pk=self.request.data.get("order", None))

    def post(self, request, *args, **kwargs):
        service = RefuseOrderService(order_repository=OrderRepository())
        service.refuse(order=self.get_object())
        return Response({"detail": "The order has been moved to HISTORY"}, status=HTTP_200_OK)
