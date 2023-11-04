from rest_framework import viewsets

from apps.read_email.models import Order
from api.serializers.read_email import OrderSerializer


class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
