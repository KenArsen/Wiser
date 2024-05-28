from drf_yasg import openapi

from apps.order.api.v1.serializers import OrderDetailSerializer

filtered_drivers_response = {
    200: openapi.Response(
        description="Filtered Drivers Response",
        schema=openapi.Schema(
            type="object",
            properties={
                "filtered_drivers": openapi.Schema(
                    type="array",
                    items=openapi.Schema(
                        type="object",
                        properties={
                            "id": openapi.Schema(type="integer"),
                            "first_name": openapi.Schema(type="string"),
                            "vehicle_type": openapi.Schema(type="string"),
                            "phone_number": openapi.Schema(type="string"),
                            "MILES OUT": openapi.Schema(type="number"),
                            "transit_time": openapi.Schema(type="number"),
                            "lat": openapi.Schema(type="number"),
                            "lon": openapi.Schema(type="number"),
                        },
                    ),
                ),
            },
        ),
    ),
}
time_until_delivery_response = {
    200: openapi.Response(
        description="Time Until Delivery Response",
        schema=openapi.Schema(
            type="object",
            properties={
                "time_until_delivery": openapi.Schema(
                    type="array",
                    items=openapi.Schema(
                        type="object",
                        properties={
                            "time_until_delivery": openapi.Schema(type="number")
                        },
                    ),
                ),
            },
        ),
    ),
}
order_data_spec = {
    "manual_parameters": [
        openapi.Parameter(
            "pick_up_at",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Pick up time",
        ),
        openapi.Parameter(
            "deliver_to",
            openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="Delivery location",
        ),
        openapi.Parameter(
            "miles", openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Miles"
        ),
    ],
    "responses": {
        200: openapi.Response("Order data description", OrderDetailSerializer)
    },
}
