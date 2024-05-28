from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, views
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.common.permissions import IsSuperAdmin
from apps.driver.api.v1.serializers import (
    DriverCreateSerializer,
    DriverDetailSerializer,
    DriverListSerializer,
    DriverUpdateSerializer,
)
from apps.driver.models import Driver
from apps.order.api.v1.serializers import TemplateSerializer
from apps.order.models import Template
from apps.vehicle.api.v1.serializers import VehicleDetailSerializer


class DriverListAPI(generics.ListAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverListSerializer
    permission_classes = (IsSuperAdmin,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class DriverDetailAPI(generics.RetrieveAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverDetailSerializer
    permission_classes = (IsSuperAdmin,)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        vehicle_data = None
        if hasattr(instance, "vehicle"):
            vehicles_serializer = VehicleDetailSerializer(instance.vehicle)
            vehicle_data = vehicles_serializer.data

        template = Template.objects.filter(is_active=True).first()
        template_serializer = TemplateSerializer(template)

        response_data = {
            "driver": serializer.data,
            "vehicle": vehicle_data,
            "template": template_serializer.data,
        }

        return Response(data=response_data)


class DriverCreateAPI(generics.CreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverCreateSerializer
    permission_classes = (IsSuperAdmin,)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DriverUpdateAPI(generics.UpdateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverUpdateSerializer
    permission_classes = (IsSuperAdmin,)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class DriverDeleteAPI(generics.DestroyAPIView):
    queryset = Driver.objects.all()
    permission_classes = (IsSuperAdmin,)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class DriverFilterAPI(generics.ListAPIView):
    queryset = Driver.objects.filter(is_available=True)
    serializer_class = DriverListSerializer
    permission_classes = (IsSuperAdmin,)

    @swagger_auto_schema(
        operation_summary="List active drivers",
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class DriverSetStatusAPI(views.APIView):
    permission_classes = (IsSuperAdmin,)

    @swagger_auto_schema(
        operation_summary="Set driver status", responses={200: "Driver Status"}
    )
    def get(self, request, pk):
        try:
            driver = Driver.objects.get(pk=pk)
            if driver.is_available:
                driver.is_available = False
            else:
                driver.is_available = True
            driver.save()
            return Response({"message": f"Driver status {driver.is_available}"})
        except Driver.DoesNotExist:
            raise ValidationError({"detail": "No such driver"})
