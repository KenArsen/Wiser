from django.db.models import Q
from rest_framework import generics

from apps.common import LargeResultsSetPagination
from apps.common.permissions import HasAccessToMyBidsPanel
from apps.order.api.v1.serializers.common import AssignSerializer
from apps.order.api.v1.serializers.my_bid import (
    MyBidDetailSerializer,
    MyBidHistorySerializer,
    MyBidListSerializer,
)
from apps.order.models import Order
from apps.order.services.my_bid import MyBidService


class BaseMyBidsView(generics.GenericAPIView):
    permission_classes = (HasAccessToMyBidsPanel,)
    pagination_class = LargeResultsSetPagination

    def get_service(self):
        return MyBidService(serializer=self.serializer_class, queryset=self.queryset)


class MyBidListAPI(BaseMyBidsView, generics.ListAPIView):
    queryset = Order.objects.filter(status="AWAITING_BID")
    serializer_class = MyBidListSerializer

    def get_queryset(self):
        return self.get_service().get_orders()


class MyBidDetailAPI(BaseMyBidsView, generics.RetrieveAPIView):
    queryset = Order.objects.filter(status="AWAITING_BID")
    serializer_class = MyBidDetailSerializer

    def get_object(self):
        return self.get_service().get_order(pk=self.kwargs["pk"])


class MyBidHistoryAPI(BaseMyBidsView, generics.ListAPIView):
    queryset = Order.objects.filter(
        Q(status="REFUSED") | Q(status="ACTIVE") | Q(status="CHECKOUT") | Q(status="COMPLETED")
    )
    serializer_class = MyBidHistorySerializer

    def get_queryset(self):
        return self.get_service().get_orders()


class AssignAPI(BaseMyBidsView):
    queryset = Order.objects.filter(status="AWAITING_BID")
    serializer_class = AssignSerializer

    def post(self, request, *args, **kwargs):
        return self.get_service().assign(data=request.data)
