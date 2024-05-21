from rest_framework import generics

from apps.common import IsAdminOrDispatcher
from apps.vehicle.api.v1.serializers import VehicleSerializer
from apps.vehicle.models import Vehicles


class VehicleListAPI(generics.ListAPIView):
    queryset = Vehicles.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = (IsAdminOrDispatcher,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class VehicleCreateAPI(generics.CreateAPIView):
    queryset = Vehicles.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = (IsAdminOrDispatcher,)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class VehicleDetailAPI(generics.RetrieveAPIView):
    queryset = Vehicles.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = (IsAdminOrDispatcher,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class VehicleUpdateAPI(generics.UpdateAPIView):
    queryset = Vehicles.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = (IsAdminOrDispatcher,)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class VehicleDeleteAPI(generics.DestroyAPIView):
    queryset = Vehicles.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = (IsAdminOrDispatcher,)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
