from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.order.api.v1.apis.order import (
    OrderFilterView,
    OrderHistoryView,
    OrderView,
    delete_all_orders,
)

app_name = "order"

router = DefaultRouter()
router.register(r"", OrderView)
router.register(r"history", OrderHistoryView, basename="orderhistory")

urlpatterns = [
    path("delete/all/", delete_all_orders),
    path("filter/", OrderFilterView.as_view(), name="order-filter"),
    path("<int:pk>/delivery-time/", OrderView.as_view({"get": "get_delivery_time"}), name="order-delivery-time"),
    path(
        "<int:pk>/location-order/",
        OrderView.as_view({"get": "get_location_order", "post": "get_location_order"}),
        name="order-location",
    ),
    path("", include(router.urls)),
]
