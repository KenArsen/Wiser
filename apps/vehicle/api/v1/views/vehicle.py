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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vehicle_repository = VehicleRepository()
        self.create_vehicle_service = VehicleCreateService(repository=self.vehicle_repository)
        self.update_vehicle_service = VehicleUpdateService(repository=self.vehicle_repository)
        self.delete_vehicle_service = VehicleDeleteService(repository=self.vehicle_repository)

    def get_object(self):
        return self.vehicle_repository.retrieve(self.kwargs["pk"])


class VehicleListAPI(BaseVehicleView, ListAPIView):
    serializer_class = VehicleListSerializer

    def get_queryset(self):
        return self.vehicle_repository.list()


class VehicleCreateAPI(BaseVehicleView, CreateAPIView):
    serializer_class = VehicleCreateSerializer

    def perform_create(self, serializer):
        serializer.instance = self.create_vehicle_service.create(serializer.validated_data)


class VehicleDetailAPI(BaseVehicleView, RetrieveAPIView):
    serializer_class = VehicleDetailSerializer


class VehicleUpdateAPI(BaseVehicleView, UpdateAPIView):
    serializer_class = VehicleUpdateSerializer

    def perform_update(self, serializer):
        serializer.instance = self.update_vehicle_service.update(
            vehicle=self.get_object(), data=serializer.validated_data
        )


class VehicleDeleteAPI(BaseVehicleView, DestroyAPIView):
    serializer_class = VehicleDetailSerializer

    def perform_destroy(self, instance):
        self.delete_vehicle_service.delete(instance)
