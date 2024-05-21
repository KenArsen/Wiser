from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.common import LargeResultsSetPagination
from apps.common.permissions import HasAccessToMyBidsPanel
from apps.order.api.v1.serializers.order_serializer import (
    AssignSerializer,
    OrderReadSerializer,
)
from apps.order.services import MyBidService, OrderService


class MyBidListAPI(generics.ListAPIView):
    serializer_class = OrderReadSerializer
    permission_classes = (HasAccessToMyBidsPanel,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return OrderService(serializer=self.serializer_class).get_filtered_orders(order_status="AWAITING_BID")


class MyBidHistoryAPI(generics.ListAPIView):
    serializer_class = OrderReadSerializer
    permission_classes = (HasAccessToMyBidsPanel,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return OrderService(serializer=self.serializer_class).get_filtered_orders(
            order_status="REFUSED", assign__isnull=True
        )


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
@permission_classes((HasAccessToMyBidsPanel,))
@api_view(["POST"])
def assign(request):
    service = MyBidService(serializer=AssignSerializer).assign(data=request.data)
    return Response(service, status=status.HTTP_200_OK)
