import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import exceptions, status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.permissions import IsAdmin, IsDispatcher
from apps.order.api.v1.serializers.order_serializer import (
    AssignSerializer,
    OrderSerializer,
)
from apps.order.models import Order
from apps.order.services import order_service


class MyBidsListAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def get(self, request, *args, **kwargs):
        queryset = Order.objects.filter(is_active=True, order_status="PENDING")
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)


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
            raise exceptions.ValidationError({"order_id": "This field is required."})
        try:
            pk = request.data["order_id"]
            order = Order.objects.get(pk=pk)
            order_service.MyBids(order=order).get_bids_yes()
            serializer = AssignSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            else:
                raise exceptions.ValidationError({"error": "Broker company/Rate confirmation not is valid"})

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
            raise exceptions.ValidationError({"order_id": "This field is required."})
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
