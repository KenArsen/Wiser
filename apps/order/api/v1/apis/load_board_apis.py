from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response

from apps.common import HasAccessToLoadBoardPanel, LargeResultsSetPagination
from apps.order.api.v1.serializers import OrderReadSerializer
from apps.order.services import LoadBoardService


class LoadBoardListAPI(generics.ListAPIView):
    serializer_class = OrderReadSerializer
    permission_classes = (HasAccessToLoadBoardPanel,)
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        return LoadBoardService(serializer=self.serializer_class).get_filtered_orders(order_status="PENDING")


class LastSimilarOrdersAPI(generics.GenericAPIView):
    serializer_class = OrderReadSerializer
    permission_classes = (HasAccessToLoadBoardPanel,)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "radius", openapi.IN_QUERY, description="Radius in miles", type=openapi.TYPE_INTEGER, default=20
            ),
            openapi.Parameter(
                "count",
                openapi.IN_QUERY,
                description="Number of nearby orders to return",
                type=openapi.TYPE_INTEGER,
                default=2,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        data, status_code = LoadBoardService(serializer=self.serializer_class).get_last_similar_orders(
            order_pk=self.kwargs["pk"],
            radius=int(request.query_params.get("radius", 20)),
        )
        return Response(data, status=status_code)
