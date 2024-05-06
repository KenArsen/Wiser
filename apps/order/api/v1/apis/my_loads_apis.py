from rest_framework import status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common import LargeResultsSetPagination
from apps.common.permissions import IsAdmin, IsDispatcher
from apps.order.api.v1.serializers import MyLoadStatusSerializer, OrderSerializer
from apps.order.models import MyLoadStatus, Order
from apps.order.repositories import MyLoadRepository


class MyLoadsListAPI(views.APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)
    pagination_class = LargeResultsSetPagination

    def get(self, request):
        queryset = MyLoadRepository.get_my_loads()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated, IsAdmin | IsDispatcher])
@api_view(["POST"])
def next_status(request):
    order_id = request.data.get("order_id")
    order = Order.objects.get(id=order_id)
    current_status = order.my_load_status.current_status

    if current_status < MyLoadStatus.Status.PAID_OFF:
        order.my_load_status.previous_status = current_status
        order.my_load_status.current_status = current_status + 1
        order.my_load_status.next_status = current_status + 2
        order.my_load_status.save()

        if order.my_load_status.current_status == MyLoadStatus.Status.DELIVERED:
            order.order_status = "CHECKOUT"
        elif order.my_load_status.current_status == MyLoadStatus.Status.PAID_OFF:
            order.order_status = "COMPLETED"

        order.save()

        serializer = MyLoadStatusSerializer(order.my_load_status)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Cannot update status."}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated, IsAdmin | IsDispatcher])
@api_view(["POST"])
def previous_status(request):
    order_id = request.data.get("order_id")
    order = Order.objects.get(id=order_id)
    current_status = order.my_load_status.current_status

    if current_status > MyLoadStatus.Status.POINT_A:
        order.my_load_status.next_status = current_status
        order.my_load_status.current_status = current_status - 1
        order.my_load_status.previous_status = current_status - 2
        order.my_load_status.save()

        if order.my_load_status.current_status < MyLoadStatus.Status.DELIVERED and order.order_status != "ASSIGN":
            order.order_status = "ASSIGN"

        order.save()

        serializer = MyLoadStatusSerializer(order.my_load_status)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Cannot update status."}, status=status.HTTP_400_BAD_REQUEST)
