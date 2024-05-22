from django.db.models import Q
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.common import LargeResultsSetPagination
from apps.common.permissions import HasAccessToMyLoadsPanel
from apps.order.api.v1.serializers import MyLoadStatusSerializer, OrderReadSerializer
from apps.order.models import Order
from apps.order.services import MyLoadService, OrderService


class MyLoadListAPI(generics.ListAPIView):
    serializer_class = OrderReadSerializer
    permission_classes = (HasAccessToMyLoadsPanel,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return OrderService(serializer=self.serializer_class).get_filtered_orders(order_status="ACTIVE")


class MyLoadHistoryAPI(generics.ListAPIView):
    serializer_class = OrderReadSerializer
    permission_classes = (HasAccessToMyLoadsPanel,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return Order.objects.filter(
            Q(order_status="REFUSED", assign__isnull=False) | Q(order_status="COMPLETED"),
        ).order_by("-updated_at", "-id")


class MyCheckoutListAPI(generics.ListAPIView):
    serializer_class = OrderReadSerializer
    permission_classes = (HasAccessToMyLoadsPanel,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return OrderService(serializer=self.serializer_class).get_filtered_orders(order_status="CHECKOUT")


class MyCompletedListAPI(generics.ListAPIView):
    serializer_class = OrderReadSerializer
    permission_classes = (HasAccessToMyLoadsPanel,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return OrderService(serializer=self.serializer_class).get_filtered_orders(order_status="COMPLETED")


@permission_classes((HasAccessToMyLoadsPanel,))
@api_view(["POST"])
def next_status(request):
    service_data, status_ = MyLoadService(serializer=MyLoadStatusSerializer).next_status(data=request.data)
    return Response(service_data, status=status_)


@permission_classes((HasAccessToMyLoadsPanel,))
@api_view(["POST"])
def previous_status(request):
    service_data, status_ = MyLoadService(serializer=MyLoadStatusSerializer).previous_status(data=request.data)
    return Response(service_data, status=status_)
