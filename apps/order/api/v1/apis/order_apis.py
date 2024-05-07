from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.paginations import LargeResultsSetPagination
from apps.common.permissions import IsAdmin, IsDispatcher
from apps.order.api.v1.serializers.order_serializer import (
    OrderReadSerializer,
    OrderSerializer,
    OrderWriteSerializer,
)
from apps.order.services import OrderService


class OrderListAPI(generics.ListAPIView):
    serializer_class = OrderReadSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return OrderService(serializer=self.serializer_class).get_orders_by_status(status_="PENDING")


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
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def get_object(self):
        return OrderService(serializer=self.serializer_class).get_order(self.kwargs["pk"])

    def destroy(self, request, *args, **kwargs):
        return Response(
            OrderService(serializer=self.serializer_class).delete_order(self.get_object()),
            status=status.HTTP_204_NO_CONTENT,
        )


class LastSimilarOrdersAPI(views.APIView):
    serializer_class = OrderReadSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "radius", openapi.IN_QUERY, description="Radius in miles", type=openapi.TYPE_INTEGER, default=20
            ),
            openapi.Parameter(
                "count",
                openapi.IN_QUERY,
                description="Number of nearby orders to return",
                type=openapi.TYPE_INTEGER,
                default=2,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        data, status_code = OrderService(serializer=self.serializer_class).get_last_similar_orders(
            order_pk=self.kwargs["pk"],
            radius=int(request.query_params.get("radius", 20)),
            count=int(request.query_params.get("count", 2)),
        )
        return Response(data, status=status_code)
