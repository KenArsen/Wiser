from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.read_email.models import Order
from api.serializers.read_email import OrderSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q


from rest_framework.permissions import IsAuthenticated
from api.utils.permissions import IsDispatcher, IsAdmin


class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher,)

    def get_delivery_time(self, request, pk=None):
        order = self.get_object()

        delivery_time = order.deliver_date_EST

        if not delivery_time:
            return Response({"error": "Delivery time not specified for the order."}, status=400)

        current_time = timezone.now()

        time_until_delivery = delivery_time - current_time

        hours, remainder = divmod(time_until_delivery.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_until_delivery_readable = f"{int(hours)}:{int(minutes)}:{int(seconds)}"

        return Response({"time_until_delivery": time_until_delivery_readable})


class OrderFilterView(APIView):

    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher,)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('pick_up_at', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Pick up time"),
            openapi.Parameter('deliver_to', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                              description="Delivery location"),
            openapi.Parameter('miles', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Miles"),
        ],
        responses={200: openapi.Response('Order data description', OrderSerializer)}
    )
    def get(self, request):
        pick_up_at = request.query_params.get('pick_up_at')
        deliver_to = request.query_params.get('deliver_to')
        miles = request.query_params.get('miles')

        filtered_orders = Order.objects.all()
        filter_conditions = Q()

        if pick_up_at:
            filter_conditions |= Q(pick_up_at__icontains=pick_up_at)
        if deliver_to:
            filter_conditions |= Q(deliver_to__icontains=deliver_to)
        if miles:
            filter_conditions |= Q(miles__exact=miles)

        if filter_conditions:
            filtered_orders = filtered_orders.filter(filter_conditions)

        serialized_data = OrderSerializer(filtered_orders, many=True)
        return Response(serialized_data.data)
