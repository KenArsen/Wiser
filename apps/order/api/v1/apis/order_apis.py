from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from apps.common.paginations import LargeResultsSetPagination
from apps.common.permissions import HasAccessToLoadBoardPanel
from apps.order.api.v1.serializers.order_serializer import (
    OrderCreateSerializer,
    OrderDetailSerializer,
    OrderListSerializer,
    OrderUpdateSerializer,
)
from apps.order.models import Order
from apps.order.services import OrderService


class OrderListAPI(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = (HasAccessToLoadBoardPanel,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return OrderService(
            serializer=self.serializer_class,
            queryset=self.queryset,
        ).get_orders()


class OrderCreateAPI(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = (HasAccessToLoadBoardPanel,)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.id
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderDetailAPI(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = (HasAccessToLoadBoardPanel,)

    def get_object(self):
        return OrderService(
            serializer=self.serializer_class,
            queryset=self.queryset,
        ).get_order(self.kwargs["pk"])


class OrderUpdateAPI(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer
    permission_classes = (HasAccessToLoadBoardPanel,)

    def get_service(self):
        return OrderService(
            serializer=self.serializer_class,
            queryset=self.queryset,
        )

    def get_object(self):
        return self.get_service().get_order(self.kwargs["pk"])

    def update(self, request, *args, **kwargs):
        order_service = self.get_service()
        updated_data = order_service.update_order(self.get_object(), request.data)
        return Response(updated_data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class OrderDeleteAPI(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = (HasAccessToLoadBoardPanel,)

    def get_service(self):
        return OrderService(
            serializer=self.serializer_class,
            queryset=self.queryset,
        )

    def get_object(self):
        return self.get_service().get_order(self.kwargs["pk"])

    def destroy(self, request, *args, **kwargs):
        service = self.get_service()
        instance = self.get_object()
        result = service.delete_order(instance)
        return Response(result, status=status.HTTP_204_NO_CONTENT)


class OrderRefuseAPI(generics.GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = (HasAccessToLoadBoardPanel,)

    def post(self, request, *args, **kwargs):
        order_id = request.data.get("order", None)
        if order_id is None:
            raise ValidationError({"detail": "order field is required."})
        service = OrderService(
            serializer=self.serializer_class,
            queryset=self.queryset,
        ).refuse_order(order_id=self.request.data["order"])
        return Response(service, status=status.HTTP_200_OK)
