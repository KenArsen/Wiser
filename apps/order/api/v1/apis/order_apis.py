from django.db.models import Q
from django.shortcuts import get_object_or_404
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
    queryset = Order.objects.filter(is_active=True, order_status="DEFAULT")
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
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(Order, pk=kwargs["pk"])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class OrderFilterView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderReadSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)
    pagination_class = LargeResultsSetPagination

    @swagger_auto_schema(
        operation_summary="Filter orders",
    )
    def get(self, request):
        pick_up_at = request.query_params.get("pick_up_at")
        deliver_to = request.query_params.get("deliver_to")
        miles = request.query_params.get("miles")
        filtered_orders = self.queryset.filter(is_active=True)
        filter_conditions = Q()
        if pick_up_at:
            filter_conditions |= Q(pick_up_at__icontains=pick_up_at)
        if deliver_to:
            filter_conditions |= Q(deliver_to__icontains=deliver_to)
        if miles:
            filter_conditions |= Q(miles__exact=miles)
        if filter_conditions:
            filtered_orders = filtered_orders.filter(filter_conditions)
        serialized_data = OrderReadSerializer(filtered_orders, many=True)
        return Response(serialized_data.data)


class LastTwoOrdersAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def get(self, request, *args, **kwargs):
        order_id = kwargs["pk"]
        order = get_object_or_404(Order, pk=order_id)

        # Получаем координаты текущего заказа
        lat_from, lon_from = order.coordinate_from.split(",")
        lat_to, lon_to = order.coordinate_to.split(",")

        # Формируем квадрат, внутри которого будем искать другие заказы
        max_latitude = float(lat_from) + 0.1  # Примерный радиус в градусах
        min_latitude = float(lat_from) - 0.1
        max_longitude = float(lon_from) + 0.1
        min_longitude = float(lon_from) - 0.1

        # Получаем другие заказы в радиусе 20 миль от текущего заказа
        other_orders = Order.objects.filter(
            ~Q(pk=order_id),  # Исключаем текущий заказ
            Q(coordinate_from__lte=max_latitude, coordinate_from__gte=min_latitude)
            & Q(coordinate_to__lte=max_latitude, coordinate_to__gte=min_latitude),
        ).order_by("-id")

        # # Инициализируем список для хранения найденных заказов
        # orders_within_20_miles = []
        #
        # # Отфильтруем заказы, расстояние между координатами которых менее 20 миль
        # for other_order in other_orders:
        #     lat_other_from, lon_other_from = other_order.coordinate_from.split(',')
        #     lat_other_to, lon_other_to = other_order.coordinate_to.split(',')
        #     lat_other_from = float(lat_other_from)
        #     lon_other_from = float(lon_other_from)
        #     lat_other_to = float(lat_other_to)
        #     lon_other_to = float(lon_other_to)
        #     distance_from = geodesic((lat_from, lon_from), (lat_other_from, lon_other_from)).miles
        #     distance_to = geodesic((lat_to, lon_to), (lat_other_to, lon_other_to)).miles
        #     if distance_from <= 20 and distance_to <= 20:
        #         orders_within_20_miles.append(other_order)
        #
        #     # Если найдено два заказа, выходим из цикла
        #     if len(orders_within_20_miles) >= 2:
        #         break

        serialized_data = OrderSerializer(other_orders, many=True)

        # return Response({"orders_within_20_miles": orders_within_20_miles})
        return Response({"orders_within_20_miles": serialized_data.data})
