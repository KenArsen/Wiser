import logging

from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.permissions import IsAdmin, IsDispatcher
from apps.order.api.v1.serializers.order_serializer import OrderSerializer
from apps.order.models import Order
from apps.order.services import order_service


class MyBidsListAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        operation_summary="List my bids",
        tags=["My Bids"],
        responses={200: OrderSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        queryset = Order.objects.filter(is_active=True, order_status="PENDING")
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)


class MyBidsDetailAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        operation_summary="Retrieve my bid details",
        tags=["My Bids"],
        responses={200: OrderSerializer()},
    )
    def get(self, request, pk, *args, **kwargs):
        order = Order.objects.get(pk=pk, is_active=True, order_status="PENDING")
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class MyBidsUpdateAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        operation_summary="Update my bid",
        tags=["My Bids"],
        request_body=OrderSerializer,
        responses={200: OrderSerializer()},
    )
    def put(self, request, pk, *args, **kwargs):
        order = get_object_or_404(Order, pk=pk, is_active=True, order_status="PENDING")
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Update my bid",
        tags=["My Bids"],
        request_body=OrderSerializer,
        responses={200: OrderSerializer()},
    )
    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk, is_active=True, order_status="PENDING")
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyBidsDeleteAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        operation_summary="Delete my bid",
        tags=["My Bids"],
        responses={204: "No Content"},
    )
    def delete(self, request, pk, *args, **kwargs):
        order = get_object_or_404(Order, pk=pk, is_active=True, order_status="PENDING")
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(
    method="post",
    tags=["My Bids"],
    operation_summary="Accept bid",
    responses={200: "Success", 400: "Bad Request"},
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["id"],
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="The ID of the order"),
        },
    ),
)
@permission_classes([IsAuthenticated, IsAdmin | IsDispatcher])
@api_view(["POST"])
def my_bids_yes(request, pk):
    if request.method == "POST":
        try:
            order = Order.objects.get(pk=pk)
            order_service.MyBids(order=order).get_bids_yes()

            return Response({"status": "The order has been moved to My Loads"}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            logging.error(f"{pk} does not exist")
            return Response({"status": "fail", "message": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return Response(
                {"status": "fail", "message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return Response({"status": "fail", "message": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="post",
    tags=["My Bids"],
    operation_summary="Reject bid",
    responses={200: "Success", 400: "Bad Request"},
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["id"],
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="The ID of the order"),
        },
    ),
)
@permission_classes([IsAuthenticated, IsAdmin | IsDispatcher])
@api_view(["POST"])
def my_bids_no(request, pk):
    if request.method == "POST":
        try:
            order = Order.objects.get(pk=pk)
            order_service.MyBids(order=order).get_bids_no()

            return Response({"status": "The order has been moved to HISTORY"}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            logging.error(f"{pk} does not exist")
            return Response({"status": "fail", "message": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return Response(
                {"status": "fail", "message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return Response({"status": "fail", "message": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
