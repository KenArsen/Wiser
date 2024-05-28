from rest_framework import generics, status
from rest_framework.response import Response

from apps.common.nominatim import get_location
from apps.common.permissions import IsSuperAdmin
from apps.vehicle.api.v1.serializers import (
    VehicleCreateSerializer,
    VehicleDetailSerializer,
    VehicleListSerializer,
    VehicleUpdateSerializer,
)
from apps.vehicle.models import Location, Vehicle


class VehicleListAPI(generics.ListAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleListSerializer
    permission_classes = (IsSuperAdmin,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class VehicleCreateAPI(generics.CreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleCreateSerializer
    permission_classes = (IsSuperAdmin,)

    def post(self, request, *args, **kwargs):
        serializer = VehicleCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        vehicle = serializer.instance
        location = get_location(vehicle.driver.address)
        Location.objects.create(
            vehicle=vehicle,
            city=location["city"],
            state=location["state"],
            county=location["county"],
            address=location["address"],
            zip_code=location["zip_code"],
            latitude=location["latitude"],
            longitude=location["longitude"],
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VehicleDetailAPI(generics.RetrieveAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleDetailSerializer
    permission_classes = (IsSuperAdmin,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class VehicleUpdateAPI(generics.UpdateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleUpdateSerializer
    permission_classes = (IsSuperAdmin,)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class VehicleDeleteAPI(generics.DestroyAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleDetailSerializer
    permission_classes = (IsSuperAdmin,)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
