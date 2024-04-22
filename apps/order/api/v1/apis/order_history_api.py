from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.common.permissions import IsAdmin, IsDispatcher
from apps.order.api.v1.serializers import OrderReadSerializer
from apps.order.models import Order


class OrderHistoryListAPI(generics.ListAPIView):
    queryset = Order.objects.filter(is_active=False)
    serializer_class = OrderReadSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)
