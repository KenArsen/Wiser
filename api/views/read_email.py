from rest_framework import generics
from apps.read_email.models import Order
from api.serializers.read_email import OrderSerializer


class OrderView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
