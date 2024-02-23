from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.common.permissions import IsAdmin, IsDispatcher
from apps.driver.api.v1.serializers.driver_serializer import DriverSerializers
from apps.driver.models import Driver


class DriverViewSet(ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializers
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)
