from rest_framework.viewsets import ModelViewSet
from apps.driver.models import Driver
from apps.driver.api.v1.serializers.driver import DriverSerializers
from rest_framework.permissions import IsAuthenticated
from apps.common.permissions import IsDispatcher, IsAdmin


class DriverViewSet(ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializers
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)
