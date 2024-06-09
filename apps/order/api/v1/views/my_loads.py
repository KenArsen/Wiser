from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)

from apps.common.paginations import LargeResultsSetPagination
from apps.common.permissions import HasAccessToMyLoadsPanel
from apps.order.api.v1.serializers.my_load import (
    MyLoadDetailSerializer,
    MyLoadListSerializer,
    MyLoadStatusSerializer,
)
from apps.order.repositories.implementations.my_load_status import (
    MyLoadStatusRepository,
)
from apps.order.repositories.implementations.order import MyLoadRepository
from apps.order.services.implementations.my_load_status import (
    MyLoadNextStatusService,
    MyLoadPreviousStatusService,
)


class BaseMyLoadAPIView(GenericAPIView):
    queryset = MyLoadRepository().none()
    permission_classes = (HasAccessToMyLoadsPanel,)
    pagination_class = LargeResultsSetPagination


class MyLoadListAPI(BaseMyLoadAPIView, ListAPIView):
    serializer_class = MyLoadListSerializer

    def get_queryset(self):
        return MyLoadRepository().list_orders()


class MyLoadDetailAPI(BaseMyLoadAPIView, RetrieveAPIView):
    serializer_class = MyLoadDetailSerializer

    def get_object(self):
        return MyLoadRepository().retrieve_order(pk=self.kwargs["pk"])


class MyLoadHistoryAPI(BaseMyLoadAPIView, ListAPIView):
    serializer_class = MyLoadListSerializer

    def get_queryset(self):
        return MyLoadRepository().get_history_orders()


class MyCheckoutListAPI(BaseMyLoadAPIView, ListAPIView):
    serializer_class = MyLoadListSerializer

    def get_queryset(self):
        return MyLoadRepository().get_checkout_orders()


class MyCompletedListAPI(BaseMyLoadAPIView, ListAPIView):
    serializer_class = MyLoadListSerializer

    def get_queryset(self):
        return MyLoadRepository().get_completed_orders()


class NextStatusAPI(BaseMyLoadAPIView, UpdateAPIView):
    serializer_class = MyLoadStatusSerializer

    def get_object(self):
        return MyLoadRepository().get_order_for_update_substatus(pk=self.request.data["order"])

    def perform_update(self, serializer):
        service = MyLoadNextStatusService(repository=MyLoadStatusRepository())
        serializer.instance = service.next_status(order=self.get_object())


class PreviousStatusAPI(BaseMyLoadAPIView, UpdateAPIView):
    serializer_class = MyLoadStatusSerializer

    def get_object(self):
        return MyLoadRepository().get_order_for_update_substatus(pk=self.request.data["order"])

    def perform_update(self, serializer):
        service = MyLoadPreviousStatusService(repository=MyLoadStatusRepository())
        serializer.instance = service.previous_status(order=self.get_object())
