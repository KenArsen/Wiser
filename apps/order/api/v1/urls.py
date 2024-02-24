from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.order.api.v1.apis import my_bids_apis, order_apis

app_name = "order"

router = DefaultRouter()
router.register(r"history", order_apis.OrderHistoryView)
router.register(r"", order_apis.OrderView)


urlpatterns = [
    path("my_bids/", my_bids_apis.MyBidsListAPI.as_view(), name="my-bids-list"),
    path("delete/all/", order_apis.delete_all_orders),
    path("filter/", order_apis.OrderFilterView.as_view(), name="order-filter"),
    path(
        "<int:pk>/delivery-time/",
        order_apis.OrderView.as_view({"get": "get_delivery_time"}),
        name="order-delivery-time",
    ),
    path(
        "<int:pk>/location-order/",
        order_apis.OrderView.as_view({"get": "get_location_order", "post": "get_location_order"}),
        name="order-location",
    ),
    path("", include(router.urls)),
]
