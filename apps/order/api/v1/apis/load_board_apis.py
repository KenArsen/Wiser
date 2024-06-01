from rest_framework import generics

from apps.common import HasAccessToLoadBoardPanel, LargeResultsSetPagination
from apps.order.api.v1.serializers import (
    LoadBoardDetailSerializer,
    LoadBoardListSerializer,
)
from apps.order.models import Order
from apps.order.services import OrderService


class BaseLoadBoardView(generics.GenericAPIView):
    pagination_class = LargeResultsSetPagination
    permission_classes = (HasAccessToLoadBoardPanel,)

    def get_service(self):
        return OrderService(
            serializer=self.serializer_class,
            queryset=self.queryset,
        )


class LoadBoardListAPI(BaseLoadBoardView, generics.ListAPIView):
    queryset = Order.objects.filter(status="PENDING")
    serializer_class = LoadBoardListSerializer

    def get_queryset(self):
        return self.get_service().get_orders()


class LoadBoardDetailAPI(BaseLoadBoardView, generics.RetrieveAPIView):
    queryset = Order.objects.filter(status="PENDING")
    serializer_class = LoadBoardDetailSerializer

    def get_object(self):
        return self.get_service().get_order(pk=self.kwargs["pk"])
