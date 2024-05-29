from rest_framework import generics

from apps.common import HasAccessToLoadBoardPanel, LargeResultsSetPagination
from apps.order.api.v1.serializers import (
    LoadBoardDetailSerializer,
    LoadBoardListSerializer,
)
from apps.order.models import Order
from apps.order.services import OrderService


class LoadBoardListAPI(generics.ListAPIView):
    queryset = Order.objects.filter(status="PENDING")
    serializer_class = LoadBoardListSerializer
    permission_classes = (HasAccessToLoadBoardPanel,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return OrderService(
            serializer=self.serializer_class,
            queryset=self.queryset,
        ).get_orders()


class LoadBoardDetailAPI(generics.RetrieveAPIView):
    queryset = Order.objects.filter(status="PENDING")
    serializer_class = LoadBoardDetailSerializer
    permission_classes = (HasAccessToLoadBoardPanel,)
    pagination_class = LargeResultsSetPagination

    def get_object(self):
        return OrderService(
            serializer=self.serializer_class,
            queryset=self.queryset,
        ).get_order(pk=self.kwargs["pk"])
