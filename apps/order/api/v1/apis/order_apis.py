from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from geopy.distance import geodesic
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
from apps.order.models import Order


class OrderListAPI(generics.ListAPIView):
    queryset = Order.objects.filter(order_status="PENDING")
    serializer_class = OrderReadSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)
    pagination_class = LargeResultsSetPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrderCreateAPI(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderWriteSerializer

    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class OrderDetailAPI(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderReadSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(self.queryset, pk=kwargs["pk"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class OrderUpdateAPI(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderWriteSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = get_object_or_404(Order, pk=kwargs["pk"])
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


class OrderDeleteAPI(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user:
            instance.order_status = "EXPIRED"
            instance.save()
            return Response({"detail": "This order has been marked as inactive."})
        else:
            self.perform_destroy(instance)
        return Response({"detail": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class LastSimilarOrdersAPI(views.APIView):
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
        order = get_object_or_404(Order, pk=kwargs["pk"])
        radius = int(request.query_params.get("radius", 20))
        count = int(request.query_params.get("count", 2))

        order_my_bids = Order.objects.filter(order_status="AWAITING_BID").order_by("-id")

        nearby_orders = []

        for bid in order_my_bids:
            distance_from = get_distance(order.coordinate_from, bid.coordinate_from)
            distance_to = get_distance(order.coordinate_to, bid.coordinate_to)

            if len(nearby_orders) >= count:
                break
            if distance_from <= radius and distance_to <= radius:
                nearby_orders.append(bid)

        serializer = OrderReadSerializer(nearby_orders, many=True)
        return Response({"nearby_orders": serializer.data}, status=status.HTTP_200_OK)


def get_distance(coord1, coord2):
    # Преобразовать координаты в кортежи чисел
    lat1, lon1 = map(float, coord1.split(","))
    lat2, lon2 = map(float, coord2.split(","))

    # Вычислить расстояние между координатами
    distance = geodesic((lat1, lon1), (lat2, lon2)).km
    return distance
