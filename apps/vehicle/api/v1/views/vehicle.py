from rest_framework import generics

from apps.common.paginations import LargeResultsSetPagination
from apps.common.permissions import IsSuperAdmin
from apps.vehicle.api.v1.serializers.vehicle import (
    VehicleCreateSerializer,
    VehicleDetailSerializer,
    VehicleListSerializer,
    VehicleUpdateSerializer,
)
from apps.vehicle.models import Vehicle


class BaseVehicleView(generics.GenericAPIView):
    queryset = Vehicle.objects.all()
    permission_classes = (IsSuperAdmin,)
    pagination_class = LargeResultsSetPagination


class VehicleListAPI(BaseVehicleView, generics.ListAPIView):
    serializer_class = VehicleListSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class VehicleCreateAPI(BaseVehicleView, generics.CreateAPIView):
    serializer_class = VehicleCreateSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class VehicleDetailAPI(BaseVehicleView, generics.RetrieveAPIView):
    serializer_class = VehicleDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class VehicleUpdateAPI(BaseVehicleView, generics.UpdateAPIView):
    serializer_class = VehicleUpdateSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class VehicleDeleteAPI(BaseVehicleView, generics.DestroyAPIView):
    serializer_class = VehicleDetailSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
