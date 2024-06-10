from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)

from apps.common.paginations import LargeResultsSetPagination
from apps.common.permissions import HasAccessToMyLoadsPanel
from apps.file.api.v1.serializers.file import ReadFileSerializer, WriteFileSerializer
from apps.file.models import File


class FileBaseView(GenericAPIView):
    queryset = File.objects.none()
    pagination_class = LargeResultsSetPagination
    permission_classes = (HasAccessToMyLoadsPanel,)


class FileListAPI(FileBaseView, ListAPIView):
    serializer_class = ReadFileSerializer

    def get_queryset(self):
        return File.objects.all()


class FileDetailAPI(FileBaseView, RetrieveAPIView):
    serializer_class = ReadFileSerializer

    def get_object(self):
        try:
            return File.objects.get(pk=self.kwargs["pk"])
        except File.DoesNotExist:
            raise ValidationError({"detail": "File does not exist"})


class FileCreateAPI(FileBaseView, CreateAPIView):
    serializer_class = WriteFileSerializer


class FileUpdateAPI(FileBaseView, UpdateAPIView):
    serializer_class = WriteFileSerializer


class FileDeleteAPI(FileBaseView, DestroyAPIView):
    serializer_class = WriteFileSerializer
