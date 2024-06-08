from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
)

from apps.common.paginations import LargeResultsSetPagination
from apps.common.permissions import HasAccessToLoadBoardPanel
from apps.order.api.v1.serializers.common import LetterSerializer
from apps.order.api.v1.serializers.load_board import (
    LoadBoardDetailSerializer,
    LoadBoardListSerializer,
)
from apps.order.repositories.implementations.letter import LetterRepository
from apps.order.repositories.implementations.order import LoadBoardRepository
from apps.order.services.implementations.letter import SendLetterService


class BaseLoadBoardView(GenericAPIView):
    queryset = LoadBoardRepository().none()
    pagination_class = LargeResultsSetPagination
    permission_classes = (HasAccessToLoadBoardPanel,)


class LoadBoardListAPI(BaseLoadBoardView, ListAPIView):
    serializer_class = LoadBoardListSerializer

    def get_queryset(self):
        return LoadBoardRepository().list()


class LoadBoardDetailAPI(BaseLoadBoardView, RetrieveAPIView):
    serializer_class = LoadBoardDetailSerializer

    def get_object(self):
        return LoadBoardRepository().get_by_id(pk=self.kwargs["pk"])


class SendEmailView(CreateAPIView):
    serializer_class = LetterSerializer

    def perform_create(self, serializer):
        SendLetterService(letter_repository=LetterRepository()).send_letter(
            data=serializer.validated_data, user=self.request.user
        )
