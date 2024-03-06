from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import IsAdmin, IsDispatcher
from apps.order.api.v1.serializers import OrderSerializer
from apps.order.models import Order


class OrderHistoryListAPI(APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        operation_summary="List order history",
        tags=["Order History"],
        operation_description="Get a list of inactive orders",
        responses={200: OrderSerializer(many=True)},
    )
    def get(self, request):
        queryset = Order.objects.all()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
