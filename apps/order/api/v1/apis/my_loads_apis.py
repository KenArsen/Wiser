from django.db.models import Q
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.common import LargeResultsSetPagination
from apps.common.permissions import HasAccessToMyLoadsPanel
from apps.order.api.v1.serializers import (
    MyLoadDetailSerializer,
    MyLoadListSerializer,
    MyLoadStatusSerializer,
)
from apps.order.models import Order
from apps.order.services import MyLoadService


class MyLoadListAPI(generics.ListAPIView):
    queryset = Order.objects.filter(status="ACTIVE")
    serializer_class = MyLoadListSerializer
    permission_classes = (HasAccessToMyLoadsPanel,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return MyLoadService(
            serializer=self.serializer_class,
            queryset=self.queryset,
        ).get_orders()


class MyLoadDetailAPI(generics.RetrieveAPIView):
    queryset = Order.objects.filter(
        Q(status="COMPLETED")
        | Q(status="CHECKOUT")
        | Q(status="ACTIVE")
        | Q(status="REFUSED", assign__isnull=False)
    )
    serializer_class = MyLoadDetailSerializer
    permission_classes = (HasAccessToMyLoadsPanel,)

    def get_object(self):
        return MyLoadService(
            serializer=self.serializer_class,
            queryset=self.queryset,
        ).get_order(pk=self.kwargs["pk"])


class MyLoadHistoryAPI(generics.ListAPIView):
    queryset = Order.objects.filter(
        Q(status="REFUSED", assign__isnull=False) | Q(status="COMPLETED")
    )
    serializer_class = MyLoadListSerializer
    permission_classes = (HasAccessToMyLoadsPanel,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return MyLoadService(
            serializer=self.serializer_class,
            queryset=self.queryset,
        ).get_orders()


class MyCheckoutListAPI(generics.ListAPIView):
    queryset = Order.objects.filter(status="CHECKOUT")
    serializer_class = MyLoadListSerializer
    permission_classes = (HasAccessToMyLoadsPanel,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return MyLoadService(
            serializer=self.serializer_class,
            queryset=self.queryset,
        ).get_orders()


class MyCompletedListAPI(generics.ListAPIView):
    queryset = Order.objects.filter(status="COMPLETED")
    serializer_class = MyLoadListSerializer
    permission_classes = (HasAccessToMyLoadsPanel,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return MyLoadService(
            serializer=self.serializer_class,
            queryset=self.queryset,
        ).get_orders()


@permission_classes((HasAccessToMyLoadsPanel,))
@api_view(["POST"])
def next_status(request):
    service_data, status_ = MyLoadService(
        serializer=MyLoadStatusSerializer,
        queryset=Order.objects.filter(
            Q(status="COMPLETED") | Q(status="CHECKOUT") | Q(status="ACTIVE")
        ),
    ).next_status(data=request.data)
    return Response(service_data, status=status_)


@permission_classes((HasAccessToMyLoadsPanel,))
@api_view(["POST"])
def previous_status(request):
    service_data, status_ = MyLoadService(
        serializer=MyLoadStatusSerializer,
        queryset=Order.objects.filter(
            Q(status="COMPLETED") | Q(status="CHECKOUT") | Q(status="ACTIVE")
        ),
    ).previous_status(data=request.data)
    return Response(service_data, status=status_)
