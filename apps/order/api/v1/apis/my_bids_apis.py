from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import exceptions, generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common import LargeResultsSetPagination
from apps.common.permissions import IsAdmin, IsDispatcher
from apps.order.api.v1.serializers.order_serializer import (
    AssignSerializer,
    OrderSerializer,
)
from apps.order.models import Order
from apps.order.repositories import MyBidRepository
from apps.order.services import MyBidService


class MyBidsListAPI(generics.ListAPIView):
    queryset = MyBidRepository.get_all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)
    pagination_class = LargeResultsSetPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class MyBidsHistoryAPI(generics.ListAPIView):
    queryset = MyBidRepository.get_all_history()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)
    pagination_class = LargeResultsSetPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


@swagger_auto_schema(
    method="post",
    operation_summary="Assign order",
    responses={200: "Success", 400: "Bad Request"},
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["id"],
        properties={
            "order_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="The ID of the order"),
            "broker_company": openapi.Schema(type=openapi.TYPE_STRING, description="The broker company "),
            "rate_confirmation": openapi.Schema(type=openapi.TYPE_STRING, description="The rate confirmation"),
        },
    ),
)
@permission_classes([IsAuthenticated, IsAdmin | IsDispatcher])
@api_view(["POST"])
def assign(request):
    if request.method == "POST":
        pk = request.data["order_id"]
        if not pk:
            raise exceptions.ValidationError({"detail": "order_id field is required."})
        try:
            order = Order.objects.get(pk=pk)
            MyBidService(order=order).get_bids_yes()
            serializer = AssignSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            else:
                raise exceptions.ValidationError({"error": "Broker company/Rate confirmation not is valid"})
            return Response({"status": "The order has been moved to My Loads"}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            raise exceptions.ValidationError({"detail": "No such order found"})
    return Response({"status": "fail", "message": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="post",
    operation_summary="Refuse order",
    responses={200: "Success", 400: "Bad Request"},
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["id"],
        properties={
            "order_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="The ID of the order"),
        },
    ),
)
@permission_classes([IsAuthenticated, IsAdmin | IsDispatcher])
@api_view(["POST"])
def refuse(request):
    if request.method == "POST":
        pk = request.data["order_id"]
        if not pk:
            raise exceptions.ValidationError({"detail": "order_id field is required."})
        try:
            order = Order.objects.get(pk=pk)
            MyBidService(order=order).get_bids_no()
            return Response({"status": "The order has been moved to HISTORY"}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            raise exceptions.ValidationError({"detail": "No such order found"})
    return Response({"status": "fail", "message": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
