from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.paginations import LargeResultsSetPagination
from apps.common.permissions import IsAdmin, IsDispatcher
from apps.order.api.v1.serializers.order_serializer import (
    OrderReadSerializer,
    OrderWriteSerializer,
)
from apps.order.models import Order
from django.db.models import Q
from apps.order.services import OrderService


class OrderListAPI(generics.ListAPIView):
    serializer_class = OrderReadSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return OrderService(serializer=self.serializer_class).get_filtered_orders(order_status="PENDING")


class OrderCreateAPI(generics.CreateAPIView):
    serializer_class = OrderWriteSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def post(self, request, *args, **kwargs):
        return Response(
            OrderService(serializer=self.serializer_class).create_order(request.data), status=status.HTTP_201_CREATED
        )


class OrderDetailAPI(generics.RetrieveAPIView):
    serializer_class = OrderReadSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def get_object(self):
        return OrderService(serializer=self.serializer_class).get_order(self.kwargs["pk"])


class OrderUpdateAPI(generics.UpdateAPIView):
    serializer_class = OrderWriteSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def get_object(self):
        return OrderService(serializer=self.serializer_class).get_order(self.kwargs["pk"])

    def update(self, request, *args, **kwargs):
        return Response(
            OrderService(serializer=self.serializer_class).update_order(self.get_object(), request.data),
            status=status.HTTP_200_OK,
        )

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class OrderDeleteAPI(generics.DestroyAPIView):
    serializer_class = OrderReadSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def get_object(self):
        return OrderService(serializer=self.serializer_class).get_order(self.kwargs["pk"])

    def destroy(self, request, *args, **kwargs):
        return Response(
            OrderService(serializer=self.serializer_class).delete_order(self.get_object()),
            status=status.HTTP_204_NO_CONTENT,
        )


class OrderRefuseAPI(generics.GenericAPIView):
    serializer_class = None
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def post(self, request, *args, **kwargs):
        service = OrderService(serializer=self.serializer_class).order_refuse(order_id=self.request.data["order_id"])
        return Response(service, status=status.HTTP_200_OK)


class MyLoadSet(generics.GenericAPIView):
    queryset = Order.objects.filter(Q(order_status='AWAITING_BID') | Q(order_status='PENDING'))

    def post(self, request, *args, **kwargs):
        for order in self.queryset.all():
            order.my_load_status.previous_status = None
            order.my_load_status.current_status = None
            order.my_load_status.next_status = None
            order.my_load_status.save()
        return Response(status=status.HTTP_200_OK)


class SetStatusAPI(generics.GenericAPIView):
    queryset = Order.objects.filter(order_status="ASSIGNED")

    def post(self, request, *args, **kwargs):
        for order in self.queryset.all():
            order.order_status = "ACTIVE"
            order.save()
        return Response(status=status.HTTP_200_OK)
