from rest_framework import generics

from apps.order.api.v1.serializers.order_serializer import OrderSerializer
from apps.order.repositories.order_repository import OrderRepository


class MyLoadsListAPI(generics.ListAPIView):
    queryset = OrderRepository.get_order_list(is_active=True, order_status="MY_LOADS")
    serializer_class = OrderSerializer


class MyLoadsDetailAPI(generics.RetrieveAPIView):
    queryset = OrderRepository.get_order_list(is_active=True, order_status="MY_LOADS")
    serializer_class = OrderSerializer


class MyLoadsUpdateAPI(generics.UpdateAPIView):
    queryset = OrderRepository.get_order_list(is_active=True)
    serializer_class = OrderSerializer


class MyLoadsDeleteAPI(generics.DestroyAPIView):
    queryset = OrderRepository.get_order_list()
    serializer_class = OrderSerializer
