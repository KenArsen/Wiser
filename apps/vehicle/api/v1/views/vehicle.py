from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)

from apps.common.paginations import LargeResultsSetPagination
from apps.common.permissions import IsSuperAdmin
from apps.vehicle.api.v1.serializers.vehicle import (
    VehicleCreateSerializer,
    VehicleDetailSerializer,
    VehicleListSerializer,
    VehicleUpdateSerializer,
)
from apps.vehicle.models import Vehicle
from apps.vehicle.repositories.implementations.vehicle import VehicleRepository
from apps.vehicle.services.implementations.vehicle import (
    VehicleCreateService,
    VehicleDeleteService,
    VehicleUpdateService,
)


class BaseVehicleView(GenericAPIView):
    queryset = Vehicle.objects.all()
    permission_classes = (IsSuperAdmin,)
    pagination_class = LargeResultsSetPagination

    def get_repository(self):
        if not hasattr(self, "_repository"):
            self._repository = VehicleRepository()
        return self._repository

    def get_object(self):
        return self.get_repository().retrieve(self.kwargs["pk"])


class VehicleListAPI(BaseVehicleView, ListAPIView):
    serializer_class = VehicleListSerializer

    def get_queryset(self):
        return self.get_repository().list()


class VehicleCreateAPI(BaseVehicleView, CreateAPIView):
    serializer_class = VehicleCreateSerializer

    def perform_create(self, serializer):
        service = VehicleCreateService(repository=self.get_repository())
        serializer.instance = service.create(serializer.validated_data)


class VehicleDetailAPI(BaseVehicleView, RetrieveAPIView):
    serializer_class = VehicleDetailSerializer


class VehicleUpdateAPI(BaseVehicleView, UpdateAPIView):
    serializer_class = VehicleUpdateSerializer

    def perform_update(self, serializer):
        service = VehicleUpdateService(repository=self.get_repository())
        serializer.instance = service.update(vehicle=self.get_object(), data=serializer.validated_data)


class VehicleDeleteAPI(BaseVehicleView, DestroyAPIView):
    serializer_class = VehicleDetailSerializer

    def perform_destroy(self, instance):
        service = VehicleDeleteService(repository=self.get_repository())
        service.delete(instance)
