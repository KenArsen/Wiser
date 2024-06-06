from rest_framework import generics
from rest_framework.response import Response

from apps.common.paginations import LargeResultsSetPagination
from apps.common.permissions import IsSuperAdmin
from apps.driver.api.v1.serializers.driver import (
    DriverAvailabilityUpdateSerializer,
    DriverCreateSerializer,
    DriverDetailSerializer,
    DriverListSerializer,
    DriverUpdateSerializer,
)
from apps.driver.models import Driver


class BaseDriverView(generics.GenericAPIView):
    queryset = Driver.objects.all()
    permission_classes = (IsSuperAdmin,)
    pagination_class = LargeResultsSetPagination


class DriverListAPI(BaseDriverView, generics.ListAPIView):
    serializer_class = DriverListSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class DriverDetailAPI(BaseDriverView, generics.RetrieveAPIView):
    serializer_class = DriverDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class DriverCreateAPI(BaseDriverView, generics.CreateAPIView):
    serializer_class = DriverCreateSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DriverUpdateAPI(BaseDriverView, generics.UpdateAPIView):
    serializer_class = DriverUpdateSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class DriverDeleteAPI(BaseDriverView, generics.DestroyAPIView):

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class DriverFilterAPI(BaseDriverView, generics.ListAPIView):
    queryset = Driver.objects.filter(is_available=True)
    serializer_class = DriverListSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class DriverAvailabilityUpdateAPI(BaseDriverView, generics.UpdateAPIView):
    serializer_class = DriverAvailabilityUpdateSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_available = not instance.is_available  # Измените значение на противоположное
        instance.save(update_fields=["is_available", "updated_at"])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
