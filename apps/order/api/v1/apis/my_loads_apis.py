from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common import LargeResultsSetPagination
from apps.common.permissions import IsAdmin, IsDispatcher
from apps.order.api.v1.serializers import MyLoadStatusSerializer, OrderReadSerializer
from apps.order.services import MyLoadService, OrderService


class MyLoadsListAPI(generics.ListAPIView):
    serializer_class = OrderReadSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return OrderService(serializer=self.serializer_class).get_orders_by_status(status_="ASSIGN")


@permission_classes([IsAuthenticated, IsAdmin | IsDispatcher])
@api_view(["POST"])
def next_status(request):
    service_data, status_ = MyLoadService(serializer=MyLoadStatusSerializer).next_status(data=request.data)
    return Response(service_data, status=status_)


@permission_classes([IsAuthenticated, IsAdmin | IsDispatcher])
@api_view(["POST"])
def previous_status(request):
    service_data, status_ = MyLoadService(serializer=MyLoadStatusSerializer).previous_status(data=request.data)
    return Response(service_data, status=status_)
