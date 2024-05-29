from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.common import LargeResultsSetPagination
from apps.common.permissions import HasAccessToMyBidsPanel
from apps.order.api.v1.serializers import (
    AssignSerializer,
    MyBidDetailSerializer,
    MyBidHistorySerializer,
    MyBidListSerializer,
)
from apps.order.models import Order
from apps.order.services import MyBidService


class MyBidListAPI(generics.ListAPIView):
    queryset = Order.objects.filter(status="AWAITING_BID")
    serializer_class = MyBidListSerializer
    permission_classes = (HasAccessToMyBidsPanel,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return MyBidService(
            serializer=self.serializer_class, queryset=self.queryset
        ).get_orders()


class MyBidDetailAPI(generics.RetrieveAPIView):
    queryset = Order.objects.filter(status="AWAITING_BID")
    serializer_class = MyBidDetailSerializer
    permission_classes = (HasAccessToMyBidsPanel,)

    def get_object(self):
        return MyBidService(
            serializer=self.serializer_class, queryset=self.get_queryset
        ).get_order(pk=self.kwargs["pk"])


class MyBidHistoryAPI(generics.ListAPIView):
    queryset = Order.objects.filter(
        Q(status="REFUSED")
        | Q(status="ACTIVE")
        | Q(status="CHECKOUT")
        | Q(status="COMPLETED")
    )
    serializer_class = MyBidHistorySerializer
    permission_classes = (HasAccessToMyBidsPanel,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return MyBidService(
            serializer=self.serializer_class, queryset=self.get_queryset
        ).get_orders()


@swagger_auto_schema(
    method="post",
    operation_summary="Assign order",
    responses={200: "Success", 400: "Bad Request"},
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["id"],
        properties={
            "order_id": openapi.Schema(
                type=openapi.TYPE_INTEGER, description="The ID of the order"
            ),
            "broker_company": openapi.Schema(
                type=openapi.TYPE_STRING, description="The broker company "
            ),
            "rate_confirmation": openapi.Schema(
                type=openapi.TYPE_STRING, description="The rate confirmation"
            ),
        },
    ),
)
@permission_classes((HasAccessToMyBidsPanel,))
@api_view(["POST"])
def assign(request):
    service = MyBidService(
        serializer=AssignSerializer,
        queryset=Order.objects.filter(status="AWAITING_BID"),
    ).assign(data=request.data)
    return Response(service, status=status.HTTP_200_OK)
