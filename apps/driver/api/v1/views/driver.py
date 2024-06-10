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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.driver_repository = DriverRepository()
        self.create_driver_service = DriverCreateService(repository=self.driver_repository)
        self.update_driver_service = DriverUpdateService(repository=self.driver_repository)
        self.delete_driver_service = DriverDeleteService(repository=self.driver_repository)
        self.driver_activate_service = DriverActivateService()
        self.driver_deactivate_service = DriverDeactivateService()

    def get_object(self):
        return self.driver_repository.retrieve(self.kwargs["pk"])


class DriverListAPI(BaseDriverView, ListAPIView):
    serializer_class = DriverListSerializer

    def get_queryset(self):
        return self.driver_repository.list()


class DriverDetailAPI(BaseDriverView, RetrieveAPIView):
    serializer_class = DriverDetailSerializer


class DriverCreateAPI(BaseDriverView, CreateAPIView):
    serializer_class = DriverCreateSerializer

    def perform_create(self, serializer):
        serializer.instance = self.create_driver_service.create(data=serializer.validated_data)


class DriverUpdateAPI(BaseDriverView, UpdateAPIView):
    serializer_class = DriverUpdateSerializer

    def perform_update(self, serializer):
        serializer.instance = self.update_driver_service.update(
            driver=self.get_object(), data=serializer.validated_data
        )


class DriverDeleteAPI(BaseDriverView, DestroyAPIView):

    def perform_destroy(self, instance):
        self.delete_driver_service.delete(instance)


class DriverFilterAPI(BaseDriverView, ListAPIView):
    serializer_class = DriverListSerializer

    def get_queryset(self):
        return self.driver_repository.get_all_active_drivers()


@method_decorator(action(detail=True, methods=["post"]), name="dispatch")
class DriverActivateAPI(BaseDriverView):
    serializer_class = DriverStatusSerializer

    def post(self, request, *args, **kwargs):
        self.driver_activate_service.activate(driver=self.get_object())
        return Response(status=HTTP_200_OK)


@method_decorator(action(detail=True, methods=["post"]), name="dispatch")
class DriverDeactivateAPI(BaseDriverView):
    serializer_class = DriverStatusSerializer

    def post(self, request, *args, **kwargs):
        self.driver_deactivate_service.deactivate(driver=self.get_object())
        return Response(status=HTTP_200_OK)
