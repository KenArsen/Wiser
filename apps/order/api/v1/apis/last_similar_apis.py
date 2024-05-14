from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.permissions import IsAdmin, IsDispatcher
from apps.order.api.v1.serializers.order_serializer import OrderReadSerializer
from apps.order.services import LastSimilarService


class LastSimilarOrdersAPI(views.APIView):
    serializer_class = OrderReadSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsDispatcher)

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
        data, status_code = LastSimilarService(serializer=self.serializer_class).get_last_similar_orders(
            order_pk=self.kwargs["pk"],
            radius=int(request.query_params.get("radius", 20)),
        )
        return Response(data, status=status_code)
