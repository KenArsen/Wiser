from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import IsAdmin, IsDispatcher
from apps.order.api.v1.serializers.order_serializer import OrderSerializer
from apps.order.repositories.order_repository import OrderRepository


class MyLoadsListAPI(APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        operation_summary="List my loads",
        tags=["My Loads"],
        operation_description="Get a list of orders with status 'MY_LOADS' made by the current user",
        responses={200: OrderSerializer(many=True)},
    )
    def get(self, request, format=None):
        queryset = OrderRepository.get_order_list(is_active=True, order_status="MY_LOADS")
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)


class MyLoadsDetailAPI(APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        operation_summary="Retrieve my load details",
        tags=["My Loads"],
        operation_description="Retrieve detailed information about an order with status"
        " 'MY_LOADS' made by the current user",
        responses={200: OrderSerializer()},
    )
    def get(self, request, pk, format=None):
        queryset = OrderRepository.get_order_list(is_active=True, order_status="MY_LOADS")
        order = queryset.get(pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class MyLoadsUpdateAPI(APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        operation_summary="Update my load",
        tags=["My Loads"],
        operation_description="Update an existing order made by the current user",
        request_body=OrderSerializer,
        responses={200: OrderSerializer()},
    )
    def put(self, request, pk, format=None):
        queryset = OrderRepository.get_order_list(is_active=True)
        order = queryset.get(pk=pk)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Update my load partially",
        tags=["My Loads"],
        operation_description="Partially update an existing order made by the current user",
        request_body=OrderSerializer,
        responses={200: OrderSerializer()},
    )
    def patch(self, request, pk, format=None):
        queryset = OrderRepository.get_order_list(is_active=True)
        order = queryset.get(pk=pk)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyLoadsDeleteAPI(APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        operation_summary="Delete my load",
        tags=["My Loads"],
        operation_description="Delete an existing order made by the current user",
        responses={204: "No Content"},
    )
    def delete(self, request, pk, format=None):
        queryset = OrderRepository.get_order_list()
        order = queryset.get(pk=pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
