from django.db.models import Q
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.common import LargeResultsSetPagination
from apps.common.permissions import HasAccessToMyLoadsPanel
from apps.order.api.v1.serializers import MyLoadListSerializer, MyLoadStatusSerializer
from apps.order.models import Order
from apps.order.services import MyLoadService


class MyLoadListAPI(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = MyLoadListSerializer
    permission_classes = (HasAccessToMyLoadsPanel,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return MyLoadService(serializer=self.serializer_class).get_filtered_orders(
            status="ACTIVE"
        )


class MyLoadHistoryAPI(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = MyLoadListSerializer
    permission_classes = (HasAccessToMyLoadsPanel,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return Order.objects.filter(
            Q(status="REFUSED", assign__isnull=False) | Q(status="COMPLETED"),
        ).order_by("-updated_at", "-id")


class MyCheckoutListAPI(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = MyLoadListSerializer
    permission_classes = (HasAccessToMyLoadsPanel,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return MyLoadService(serializer=self.serializer_class).get_filtered_orders(
            status="CHECKOUT"
        )


class MyCompletedListAPI(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = MyLoadListSerializer
    permission_classes = (HasAccessToMyLoadsPanel,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return MyLoadService(serializer=self.serializer_class).get_filtered_orders(
            status="COMPLETED"
        )


@permission_classes((HasAccessToMyLoadsPanel,))
@api_view(["POST"])
def next_status(request):
    service_data, status_ = MyLoadService(
        serializer=MyLoadStatusSerializer
    ).next_status(data=request.data)
    return Response(service_data, status=status_)


@permission_classes((HasAccessToMyLoadsPanel,))
@api_view(["POST"])
def previous_status(request):
    service_data, status_ = MyLoadService(
        serializer=MyLoadStatusSerializer
    ).previous_status(data=request.data)
    return Response(service_data, status=status_)
