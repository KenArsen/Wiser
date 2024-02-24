from rest_framework import status, views
from rest_framework.response import Response

from apps.order.api.v1.serializers import order_serializer
from apps.order.repositories import order_repository


class MyBidsListAPI(views.APIView):
    def get(self, request):
        queryset = order_repository.OrderRepository.get_order_list(is_active=True, order_status="PENDING")
        serializer = order_serializer.OrderSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
