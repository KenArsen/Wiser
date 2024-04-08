from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.permissions import IsAdmin, IsDispatcher
from apps.order.api.v1.serializers import OrderReadSerializer, OrderWriteSerializer
from apps.order.models import Order


class OrderHistoryListAPI(generics.ListAPIView):
    queryset = Order.objects.filter(is_active=False)
    serializer_class = OrderReadSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)


class OrderHistoryDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.filter(is_active=False)
    serializer_class = OrderReadSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def retrieve(self, request, *args, **kwargs):
        instance = self.queryset(pk=kwargs['pk'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class OrderHistoryUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderWriteSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        order = get_object_or_404(Order, pk=kwargs['pk'], is_active=False)
        serializer = self.get_serializer(order, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class OrderHistoryDeleteAPI(generics.DestroyAPIView):
    queryset = Order.objects.filter(is_active=False)
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
