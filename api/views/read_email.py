from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.read_email.models import Order
from api.serializers.read_email import OrderSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q


class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderFilterView(APIView):

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
