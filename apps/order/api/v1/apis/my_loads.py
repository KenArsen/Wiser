from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.permissions import IsAdmin, IsDispatcher
from apps.order.api.v1.serializers import OrderSerializer
from apps.order.models import Order


class MyLoadsListAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        operation_summary="List my loads",
        tags=["My Loads"],
        operation_description="Get a list of orders with status 'MY_LOADS' made by the current user",
        responses={200: OrderSerializer(many=True)},
    )
    def get(self, request):
        queryset = Order.objects.filter(is_active=True, order_status="MY_LOADS")
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyLoadsStatus(views.APIView):
    @swagger_auto_schema(
        tags=["My Loads"],
        responses={
            200: "Order status updated successfully",
            400: "Invalid new status or Order is already in CHECKOUT status",
            404: "Order does not exist"
        },
        operation_summary="Update order status",
        operation_description="Update the status of the order identified by the provided pk to the next status",
    )
    def post(self, request, pk):

        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND)

        current_status = order.my_loads_status
        if current_status == Order.MyLoadsStatus.CHECKOUT:
            return Response({"error": "Order is already in CHECKOUT status"}, status=status.HTTP_400_BAD_REQUEST)

        next_status = current_status + 1

        if next_status > Order.MyLoadsStatus.CHECKOUT:
            return Response({"error": "Invalid new status"}, status=status.HTTP_400_BAD_REQUEST)

        order.my_loads_status = next_status
        order.save()

        return Response(
            {
                "message": "Order status updated successfully",
                'status': order.my_loads_status
            }, status=status.HTTP_200_OK)
