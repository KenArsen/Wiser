from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views, exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.permissions import IsAdmin, IsDispatcher
from apps.order.api.v1.serializers import OrderSerializer
from apps.order.models import Order


class MyLoadsListAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def get(self, request):
        queryset = Order.objects.filter(is_active=True, order_status="MY_LOADS", my_loads_status__lte=5)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyLoadsCheckoutAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def get(self, request):
        queryset = Order.objects.filter(is_active=True, order_status="MY_LOADS", my_loads_status=6)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyLoadsCompletedAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def get(self, request):
        queryset = Order.objects.filter(is_active=True, order_status="MY_LOADS", my_loads_status=7)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyLoadsDetailAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, is_active=True, order_status="MY_LOADS")
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class MyLoadsUpdateAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def put(self, request, pk):
        order = get_object_or_404(Order, pk=pk, is_active=True, order_status="MY_LOADS")
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk, is_active=True, order_status="MY_LOADS")
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyLoadsDeleteAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def delete(self, request, pk):
        get_object_or_404(Order, pk=pk, is_active=True, order_status="MY_LOADS").delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyLoadsStatus(views.APIView):
    @swagger_auto_schema(
        operation_summary="Update order status",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "order_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="The ID of the order"),
            },
            required=["order_id"]
        ),
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "status": openapi.Schema(type=openapi.TYPE_STRING, description="Status of the order")})),
        }
    )
    def post(self, request):
        pk = request.data.get("order_id")
        if not pk:
            raise exceptions.ValidationError({"order_id": "This field is required."})

        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND)

        current_status = order.my_loads_status
        if current_status == Order.MyLoadsStatus.COMPLETED:
            return Response({"error": "Order is already in COMPLETED status"}, status=status.HTTP_400_BAD_REQUEST)

        next_status = current_status + 1

        if next_status > Order.MyLoadsStatus.COMPLETED:
            return Response({"error": "Invalid new status"}, status=status.HTTP_400_BAD_REQUEST)

        order.my_loads_status = next_status
        order.save()

        return Response({"status": order.get_my_loads_status_display()}, status=status.HTTP_200_OK)
