from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.common import IsAdmin, IsDispatcher
from apps.vehicle.api.v1.serializers import VehicleSerializer
from apps.vehicle.models import Vehicles


class VehicleListAPI(generics.ListAPIView):
    queryset = Vehicles.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        operation_summary="List drivers",
        tags=["Vehicles"],
        responses={200: VehicleSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class VehicleCreateAPI(generics.CreateAPIView):
    queryset = Vehicles.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        operation_summary="Create new a vehicle",
        tags=["Vehicles"],
        responses={201: VehicleSerializer()},
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class VehicleDetailAPI(generics.RetrieveAPIView):
    queryset = Vehicles.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        operation_summary="Retrieve vehicle details",
        tags=["Vehicles"],
        responses={200: VehicleSerializer()},
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class VehicleUpdateAPI(generics.UpdateAPIView):
    queryset = Vehicles.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        operation_summary="Update the vehicle",
        tags=["Vehicles"],
        request_body=VehicleSerializer,
        responses={200: VehicleSerializer()},
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update the vehicle",
        tags=["Vehicles"],
        request_body=VehicleSerializer,
        responses={200: VehicleSerializer()},
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class VehicleDeleteAPI(generics.DestroyAPIView):
    queryset = Vehicles.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        operation_summary="Delete the vehicle",
        tags=["Vehicles"],
        responses={201: "No content"},
    )
    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
