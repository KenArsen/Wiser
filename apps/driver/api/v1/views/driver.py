from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from apps.common.paginations import LargeResultsSetPagination
from apps.common.permissions import IsSuperAdmin
from apps.driver.api.v1.serializers.driver import (
    DriverCreateSerializer,
    DriverDetailSerializer,
    DriverListSerializer,
    DriverStatusSerializer,
    DriverUpdateSerializer,
)
from apps.driver.repositories.implementations.driver import DriverRepository
from apps.driver.services.implementations.driver import (
    DriverActivateService,
    DriverCreateService,
    DriverDeactivateService,
    DriverDeleteService,
    DriverUpdateService,
)


class BaseDriverView(GenericAPIView):
    queryset = DriverRepository().none()
    permission_classes = (IsSuperAdmin,)
    pagination_class = LargeResultsSetPagination

    def get_repository(self):
        if not hasattr(self, "_repository"):
            self._repository = DriverRepository()
        return self._repository

    def get_object(self):
        return self.get_repository().retrieve(self.kwargs["pk"])


class DriverListAPI(BaseDriverView, ListAPIView):
    serializer_class = DriverListSerializer

    def get_queryset(self):
        return self.get_repository().list()


class DriverDetailAPI(BaseDriverView, RetrieveAPIView):
    serializer_class = DriverDetailSerializer


class DriverCreateAPI(BaseDriverView, CreateAPIView):
    serializer_class = DriverCreateSerializer

    def perform_create(self, serializer):
        service = DriverCreateService(repository=self.get_repository())
        serializer.instance = service.create(data=serializer.validated_data)


class DriverUpdateAPI(BaseDriverView, UpdateAPIView):
    serializer_class = DriverUpdateSerializer

    def perform_update(self, serializer):
        service = DriverUpdateService(repository=self.get_repository())
        serializer.instance = service.update(driver=self.get_object(), data=serializer.validated_data)


class DriverDeleteAPI(BaseDriverView, DestroyAPIView):

    def perform_destroy(self, instance):
        service = DriverDeleteService(repository=self.get_repository())
        service.delete(instance)


class DriverFilterAPI(BaseDriverView, ListAPIView):
    serializer_class = DriverListSerializer

    def get_queryset(self):
        return self.get_repository().get_all_active_drivers()


@method_decorator(action(detail=True, methods=["post"]), name="dispatch")
class DriverActivateAPI(BaseDriverView):
    serializer_class = DriverStatusSerializer

    def post(self, request, *args, **kwargs):
        DriverActivateService().activate(driver=self.get_object())
        return Response(status=HTTP_200_OK)


@method_decorator(action(detail=True, methods=["post"]), name="dispatch")
class DriverDeactivateAPI(BaseDriverView):
    serializer_class = DriverStatusSerializer

    def post(self, request, *args, **kwargs):
        DriverDeactivateService().deactivate(driver=self.get_object())
        return Response(status=HTTP_200_OK)
