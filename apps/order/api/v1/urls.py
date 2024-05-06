from django.urls import path

from apps.order.api.v1.apis import (
    LastSimilarOrdersAPI,
    MyBidsHistoryAPI,
    MyBidsListAPI,
    MyLoadsListAPI,
    OrderCreateAPI,
    OrderDeleteAPI,
    OrderDetailAPI,
    OrderListAPI,
    OrderUpdateAPI,
    assign,
    next_status,
    previous_status,
    refuse,
)

from .apis.get_location_apis import GetLocationAPI

app_name = "orders"

urlpatterns = [
    path("", OrderListAPI.as_view(), name="order-list"),
    path("create/", OrderCreateAPI.as_view(), name="order-create"),
    path("<int:pk>/", OrderDetailAPI.as_view(), name="order-detail"),
    path("<int:pk>/update/", OrderUpdateAPI.as_view(), name="order-update"),
    path("<int:pk>/delete/", OrderDeleteAPI.as_view(), name="order-delete"),
    # path("get_location/", GetLocationAPI.as_view(), name="get-location-drivers"),
    path("last_similar/<int:pk>/", LastSimilarOrdersAPI.as_view(), name="last-similar-orders"),
]

# my bids
urlpatterns += [
    path("my_bids/", MyBidsListAPI.as_view(), name="my-bids-list"),
    path("my_bids/history/", MyBidsHistoryAPI.as_view(), name="my-bids-history"),
    path("my_bids/assign/", assign, name="my-bids-assign"),
    path("my_bids/refuse/", refuse, name="my-bids-refuse"),
]

# my loads
urlpatterns += [
    path("my_loads/", MyLoadsListAPI.as_view(), name="my-loads"),
    path("my_loads/next_status/", next_status, name="next-status"),
    path("my_loads/previous_status/", previous_status, name="previous-status"),
]
