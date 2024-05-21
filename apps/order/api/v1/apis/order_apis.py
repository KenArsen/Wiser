from rest_framework import generics, status
from rest_framework.response import Response

from apps.common.paginations import LargeResultsSetPagination
from apps.common.permissions import IsAdminOrDispatcher
from apps.order.api.v1.serializers.order_serializer import (
    OrderReadSerializer,
    OrderWriteSerializer,
)
from apps.order.services import OrderService


class OrderListAPI(generics.ListAPIView):
    serializer_class = OrderReadSerializer
    permission_classes = (IsAdminOrDispatcher,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return OrderService(serializer=self.serializer_class).get_filtered_orders(order_status="PENDING")


class OrderCreateAPI(generics.CreateAPIView):
    serializer_class = OrderWriteSerializer
    permission_classes = (IsAdminOrDispatcher,)

    def post(self, request, *args, **kwargs):
        return Response(
            OrderService(serializer=self.serializer_class).create_order(request.data), status=status.HTTP_201_CREATED
        )


class OrderDetailAPI(generics.RetrieveAPIView):
    serializer_class = OrderReadSerializer
    permission_classes = (IsAdminOrDispatcher,)

    def get_object(self):
        return OrderService(serializer=self.serializer_class).get_order(self.kwargs["pk"])


class OrderUpdateAPI(generics.UpdateAPIView):
    serializer_class = OrderWriteSerializer
    permission_classes = (IsAdminOrDispatcher,)

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
    permission_classes = (IsAdminOrDispatcher,)

    def get_object(self):
        return OrderService(serializer=self.serializer_class).get_order(self.kwargs["pk"])

    def destroy(self, request, *args, **kwargs):
        return Response(
            OrderService(serializer=self.serializer_class).delete_order(self.get_object()),
            status=status.HTTP_204_NO_CONTENT,
        )


class OrderRefuseAPI(generics.GenericAPIView):
    serializer_class = None
    permission_classes = (IsAdminOrDispatcher,)

    def post(self, request, *args, **kwargs):
        service = OrderService(serializer=self.serializer_class).order_refuse(order_id=self.request.data["order_id"])
        return Response(service, status=status.HTTP_200_OK)
