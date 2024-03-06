from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import IsAdmin, IsDispatcher
from apps.order.api.v1.serializers import OrderSerializer
from apps.order.repositories import OrderRepository


class MyLoadsListAPI(APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        operation_summary="List my loads",
        tags=["My Loads"],
        operation_description="Get a list of orders with status 'MY_LOADS' made by the current user",
        responses={200: OrderSerializer(many=True)},
    )
    def get(self, request):
        queryset = OrderRepository.get_order_list(is_active=True, order_status="MY_LOADS")
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
