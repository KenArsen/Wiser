from django.shortcuts import get_object_or_404
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
        responses={200: OrderSerializer(many=True)},
    )
    def get(self, request):
        queryset = Order.objects.filter(is_active=False)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderHistoryDetailView(APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        operation_summary="Retrieve an order",
        tags=["Order History"],
        responses={200: OrderSerializer()},
    )
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, is_active=False)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderHistoryUpdateView(APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        operation_summary="Update an order",
        tags=["Order History"],
        request_body=OrderSerializer,
        responses={200: OrderSerializer()},
    )
    def put(self, request, pk):
        order = get_object_or_404(Order, pk=pk, is_active=False)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Partially update an order",
        tags=["Order History"],
        request_body=OrderSerializer,
        responses={200: OrderSerializer()},
    )
    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk, is_active=False)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderHistoryDeleteAPI(APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        operation_summary="Delete an order",
        tags=["Order History"],
        responses={204: "No Content"},
    )
    def delete(self, request, pk):
        order = get_object_or_404(Order, pk=pk, is_active=False)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
