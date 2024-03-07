from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.permissions import IsAdmin, IsDispatcher
from apps.driver.api.v1.serializers import DriverSerializers
from apps.driver.models import Driver


class DriverListAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        operation_summary="List drivers",
        tags=["Drivers"],
        responses={200: DriverSerializers(many=True)},
    )
    def get(self, request, *args, **kwargs):
        queryset = Driver.objects.all()
        serializer = DriverSerializers(queryset, many=True)
        return Response(serializer.data)


class DriverDetailAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        operation_summary="Retrieve driver details",
        tags=["Drivers"],
        responses={200: DriverSerializers()},
    )
    def get(self, request, pk, *args, **kwargs):
        try:
            driver = Driver.objects.get(pk=pk)
            serializer = DriverSerializers(driver)
            return Response(serializer.data)
        except Driver.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DriverCreateAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        operation_summary="Create a new driver",
        tags=["Drivers"],
        request_body=DriverSerializers,
        responses={201: DriverSerializers()},
    )
    def post(self, request, *args, **kwargs):
        serializer = DriverSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DriverUpdateAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    @swagger_auto_schema(
        operation_summary="Update driver",
        tags=["Drivers"],
        request_body=DriverSerializers,
        responses={200: DriverSerializers()},
    )
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

    @swagger_auto_schema(
        operation_summary="Update a driver",
        tags=["Drivers"],
        request_body=DriverSerializers,
        responses={200: DriverSerializers()},
    )
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

    @swagger_auto_schema(
        operation_summary="Delete a driver",
        tags=["Drivers"],
        responses={204: "No Content"},
    )
    def delete(self, request, pk, *args, **kwargs):
        try:
            driver = Driver.objects.get(pk=pk)
            driver.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Driver.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
