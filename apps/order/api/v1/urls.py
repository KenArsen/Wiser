from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.order.api.v1.apis.my_bids_apis import (
    MyBidsDeleteAPI,
    MyBidsDetailAPI,
    MyBidsListAPI,
    MyBidsUpdateAPI,
    my_bids_no,
    my_bids_yes,
)
from apps.order.api.v1.apis.my_loads import (
    MyLoadsDeleteAPI,
    MyLoadsDetailAPI,
    MyLoadsListAPI,
    MyLoadsUpdateAPI,
)
from apps.order.api.v1.apis.order_apis import (  # OrderHistoryView,
    OrderFilterView,
    OrderView,
    delete_all_orders,
)
from apps.order.api.v1.apis.order_history_api import (
    OrderHistoryDeleteAPI,
    OrderHistoryDetailView,
    OrderHistoryListAPI,
    OrderHistoryUpdateView,
)

app_name = "orders"

router = DefaultRouter()
router.register(r"", OrderView)

urlpatterns = [
    path("delete/all/", delete_all_orders),
    path("filter/", OrderFilterView.as_view(), name="order-filter"),
    path(
        "<int:pk>/delivery-time/",
        OrderView.as_view({"get": "get_delivery_time"}),
        name="order-delivery-time",
    ),
    path(
        "<int:pk>/location-order/",
        OrderView.as_view({"get": "get_location_order", "post": "get_location_order"}),
        name="order-location",
    ),
]

# order-history
urlpatterns += [
    path("history/", OrderHistoryListAPI.as_view(), name="order-history-list"),
    path("history/<int:pk>/", OrderHistoryDetailView.as_view(), name="order-history-detail"),
    path("history/<int:pk>/update/", OrderHistoryUpdateView.as_view(), name="order-history-update"),
    path("history/<int:pk>/delete/", OrderHistoryDeleteAPI.as_view(), name="order-history-delete"),
]

# my bids
urlpatterns += [
    path("my_bids/", MyBidsListAPI.as_view(), name="my-bids-list"),
    path("my_bids/<int:pk>/", MyBidsDetailAPI.as_view(), name="my-bids-detail"),
    path("my_bids/<int:pk>/update/", MyBidsUpdateAPI.as_view(), name="my-bids-update"),
    path("my_bids/<int:pk>/delete/", MyBidsDeleteAPI.as_view(), name="my-bids-delete"),
    path("my_bids/<int:pk>/yes/", my_bids_yes, name="my-bids-yes"),
    path("my_bids/<int:pk>/no/", my_bids_no, name="my-bids-no"),
]

# my loads
urlpatterns += [
    path("my_loads/", MyLoadsListAPI.as_view(), name="my-loads"),
    path("my_loads/<int:pk>/", MyLoadsDetailAPI.as_view(), name="my-loads-detail"),
    path("my_loads/<int:pk>/update/", MyLoadsUpdateAPI.as_view(), name="my-loads-update"),
    path("my_loads/<int:pk>/delete/", MyLoadsDeleteAPI.as_view(), name="my-loads-delete"),
]

# routers
urlpatterns += router.urls
