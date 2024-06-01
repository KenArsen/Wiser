from django.db.models import Q
from rest_framework import generics
from rest_framework.response import Response

from apps.common.paginations import LargeResultsSetPagination
from apps.common.permissions import HasAccessToMyLoadsPanel
from apps.order.api.v1.serializers import (
    MyLoadDetailSerializer,
    MyLoadListSerializer,
    MyLoadStatusSerializer,
)
from apps.order.models import Order
from apps.order.services import MyLoadService


class BaseMyLoadAPIView(generics.GenericAPIView):
    permission_classes = (HasAccessToMyLoadsPanel,)
    pagination_class = LargeResultsSetPagination

    def get_service(self):
        return MyLoadService(
            serializer=self.serializer_class,
            queryset=self.queryset,
        )


class MyLoadListAPI(BaseMyLoadAPIView, generics.ListAPIView):
    queryset = Order.objects.filter(status="ACTIVE")
    serializer_class = MyLoadListSerializer

    def get_queryset(self):
        return self.get_service().get_orders()


class MyLoadDetailAPI(BaseMyLoadAPIView, generics.RetrieveAPIView):
    queryset = Order.objects.filter(
        Q(status="COMPLETED") | Q(status="CHECKOUT") | Q(status="ACTIVE") | Q(status="REFUSED", assign__isnull=False)
    )
    serializer_class = MyLoadDetailSerializer

    def get_object(self):
        return self.get_service().get_order(pk=self.kwargs["pk"])


class MyLoadHistoryAPI(BaseMyLoadAPIView, generics.ListAPIView):
    queryset = Order.objects.filter(Q(status="REFUSED", assign__isnull=False) | Q(status="COMPLETED"))
    serializer_class = MyLoadListSerializer

    def get_queryset(self):
        return self.get_service().get_orders()


class MyCheckoutListAPI(BaseMyLoadAPIView, generics.ListAPIView):
    queryset = Order.objects.filter(status="CHECKOUT")
    serializer_class = MyLoadListSerializer

    def get_queryset(self):
        return self.get_service().get_orders()


class MyCompletedListAPI(BaseMyLoadAPIView, generics.ListAPIView):
    queryset = Order.objects.filter(status="COMPLETED")
    serializer_class = MyLoadListSerializer

    def get_queryset(self):
        return self.get_service().get_orders()


class NextStatusAPI(BaseMyLoadAPIView):
    queryset = Order.objects.filter(Q(status="COMPLETED") | Q(status="CHECKOUT") | Q(status="ACTIVE"))
    serializer_class = MyLoadStatusSerializer

    def post(self, request, *args, **kwargs):
        service_data, status_ = self.get_service().next_status(data=request.data)
        return Response(service_data, status=status_)


class PreviousStatusAPI(BaseMyLoadAPIView):
    queryset = Order.objects.filter(Q(status="COMPLETED") | Q(status="CHECKOUT") | Q(status="ACTIVE"))
    serializer_class = MyLoadStatusSerializer

    def post(self, request, *args, **kwargs):
        service_data, status_ = self.get_service().previous_status(data=request.data)
        return Response(service_data, status=status_)
