from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
)

from apps.common.paginations import LargeResultsSetPagination
from apps.common.permissions import HasAccessToMyBidsPanel
from apps.order.api.v1.serializers.common import AssignSerializer
from apps.order.api.v1.serializers.my_bid import (
    MyBidDetailSerializer,
    MyBidHistorySerializer,
    MyBidListSerializer,
)
from apps.order.repositories.implementations.assign import AssignRepository
from apps.order.repositories.implementations.order import MyBidRepository
from apps.order.services.implementations.order import AssignOrderService


class BaseMyBidsView(GenericAPIView):
    queryset = MyBidRepository().none()
    permission_classes = (HasAccessToMyBidsPanel,)
    pagination_class = LargeResultsSetPagination

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.my_bid_repository = MyBidRepository()

    def get_object(self):
        return self.my_bid_repository.retrieve_order(pk=self.kwargs["pk"])


class MyBidListAPI(BaseMyBidsView, ListAPIView):
    serializer_class = MyBidListSerializer

    def get_queryset(self):
        return self.my_bid_repository.list_orders()


class MyBidDetailAPI(BaseMyBidsView, RetrieveAPIView):
    serializer_class = MyBidDetailSerializer


class MyBidHistoryAPI(BaseMyBidsView, ListAPIView):
    serializer_class = MyBidHistorySerializer

    def get_queryset(self):
        return self.my_bid_repository.get_history_orders()


class AssignAPI(CreateAPIView):
    permission_classes = (HasAccessToMyBidsPanel,)
    serializer_class = AssignSerializer

    def perform_create(self, serializer):
        service = AssignOrderService(repository=AssignRepository())
        serializer.instance = service.assign_order(data=serializer.validated_data)
