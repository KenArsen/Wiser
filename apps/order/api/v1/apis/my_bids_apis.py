import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.order.api.v1.serializers.order_serializer import OrderSerializer
from apps.order.models import Order
from apps.order.repositories.order_repository import OrderRepository
from apps.order.services import order_service


class MyBidsListAPI(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderRepository.get_order_list(is_active=True, order_status="PENDING")


class MyBidsDetailAPI(generics.RetrieveAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderRepository.get_order_list(is_active=True, order_status="PENDING")

    def get_object(self):
        queryset = self.get_queryset()
        pk = self.kwargs["pk"]
        return queryset.get(pk=pk)


class MyBidsUpdateAPI(generics.UpdateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderRepository.get_order_list(is_active=True, order_status="PENDING")

    def get_object(self):
        queryset = self.get_queryset()
        pk = self.kwargs["pk"]
        return queryset.get(pk=pk)


class MyBidsDeleteAPI(generics.DestroyAPIView):
    def get_queryset(self):
        return OrderRepository.get_order_list(is_active=True, order_status="PENDING")

    def get_object(self):
        queryset = self.get_queryset()
        pk = self.kwargs["pk"]
        return queryset.get(pk=pk)


@swagger_auto_schema(
    method="post",
    operation_summary="Accept bid",
    operation_description="This endpoint accepts the bid for the order.",
    responses={200: "Success", 400: "Bad Request"},
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["id"],
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="The ID of the order"),
        },
    ),
)
@api_view(["POST"])
def my_bids_yes(request, pk):
    if request.method == "POST":
        try:
            order = Order.objects.get(pk=pk)
            order_service.MyBids(order=order).get_bids_yes()

            return Response({"status": "success"}, status=status.HTTP_200_OK)
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
    operation_summary="Reject bid",
    operation_description="This endpoint rejects the bid for the order.",
    responses={200: "Success", 400: "Bad Request"},
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["id"],
        properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="The ID of the order"),
        },
    ),
)
@api_view(["POST"])
def my_bids_no(request, pk):
    if request.method == "POST":
        try:
            order = Order.objects.get(pk=pk)
            order_service.MyBids(order=order).get_bids_no()

            return Response({"status": "success"}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            logging.error(f"{pk} does not exist")
            return Response({"status": "fail", "message": "Order does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return Response(
                {"status": "fail", "message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return Response({"status": "fail", "message": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
