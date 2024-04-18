from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, views
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.permissions import IsAdmin, IsDispatcher
from apps.driver.api.v1.serializers import DriverSerializers
from apps.driver.models import Driver
from apps.order.api.v1.serializers import TemplateSerializer
from apps.order.models import Template
from apps.vehicle.api.v1.serializers import VehicleSerializer


class DriverListAPI(generics.ListAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializers
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class DriverDetailAPI(generics.RetrieveAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializers
    permission_classes = [IsAuthenticated, IsAdmin | IsDispatcher]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        vehicles_serializer = VehicleSerializer(instance.driver_vehicles.all(), many=True)
        template = Template.objects.filter(is_active=True).first()
        template_serializer = TemplateSerializer(template)
        return Response(
            data={"driver": serializer.data, "vehicles": vehicles_serializer.data, "template": template_serializer.data}
        )


class DriverCreateAPI(generics.CreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializers
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DriverUpdateAPI(generics.UpdateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializers
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class DriverDeleteAPI(generics.DestroyAPIView):
    queryset = Driver.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class DriverFilterAPI(generics.ListAPIView):
    queryset = Driver.objects.filter(is_active=True)
    serializer_class = DriverSerializers
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        operation_summary="List active drivers",
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class DriverSetStatusAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(operation_summary="Set driver status", responses={200: "Driver Status"})
    def get(self, request, pk):
        try:
            driver = Driver.objects.get(pk=pk)
            if driver.is_active:
                driver.is_active = False
            else:
                driver.is_active = True
            driver.save()
            return Response({"message": f"Driver status {driver.is_active}"})
        except Driver.DoesNotExist:
            raise ValidationError({"detail": "No such driver"})
