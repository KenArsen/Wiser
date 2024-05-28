from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response

from apps.common import HasAccessToLoadBoardPanel, LargeResultsSetPagination
from apps.order.api.v1.serializers import (
    LoadBoardDetailSerializer,
    LoadBoardListSerializer,
)
from apps.order.models import Order
from apps.order.services import LoadBoardService


class LoadBoardListAPI(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = LoadBoardListSerializer
    permission_classes = (HasAccessToLoadBoardPanel,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return LoadBoardService(serializer=self.serializer_class).get_filtered_orders(
            status="PENDING"
        )


class LoadBoardDetailAPI(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = LoadBoardDetailSerializer
    permission_classes = (HasAccessToLoadBoardPanel,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return LoadBoardService(serializer=self.serializer_class).get_filtered_orders(
            status="PENDING"
        )
