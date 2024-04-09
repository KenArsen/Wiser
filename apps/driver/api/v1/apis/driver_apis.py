from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.permissions import IsAdmin, IsDispatcher
from apps.driver.api.v1.serializers import DriverSerializers
from apps.vehicle.api.v1.serializers import VehicleSerializer
from apps.driver.models import Driver
from apps.order.models import Template
from apps.order.api.v1.serializers import TemplateSerializer


class DriverListAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def get(self, request, *args, **kwargs):
        queryset = Driver.objects.all()
        serializer = DriverSerializers(queryset, many=True)
        return Response(serializer.data)


class DriverDetailAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def get(self, request, pk, *args, **kwargs):
        try:
            driver = Driver.objects.prefetch_related('vehicles').get(pk=pk)
            vehicles = driver.vehicles.all()
            vehicles_serializer = VehicleSerializer(vehicles, many=True)
            serializer = DriverSerializers(driver)
            template = Template.objects.filter(is_active=True).first()
            template_serializer = TemplateSerializer(template)
            return Response(data={"driver": serializer.data, "vehicles": vehicles_serializer.data,
                                  "template": template_serializer.data})
        except Driver.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DriverCreateAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def post(self, request, *args, **kwargs):
        serializer = DriverSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DriverUpdateAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def put(self, request, pk, *args, **kwargs):
        try:
            driver = Driver.objects.get(pk=pk)
        except Driver.DoesNotExist:
            return Response({"error": "Driver not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DriverSerializers(driver, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            driver = Driver.objects.get(pk=pk)
            serializer = DriverSerializers(driver, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Driver.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DriverDeleteAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def delete(self, request, pk, *args, **kwargs):
        try:
            driver = Driver.objects.get(pk=pk)
            driver.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Driver.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DriverFilterAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        operation_summary="List active drivers",
    )
    def get(self, request, *args, **kwargs):
        queryset = Driver.objects.filter(is_active=True)
        serializer = DriverSerializers(queryset, many=True)
        return Response(serializer.data)


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
