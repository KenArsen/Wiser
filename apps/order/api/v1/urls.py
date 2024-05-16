from django.urls import path

from apps.order.api.v1.apis import (
    LastSimilarOrdersAPI,
    MyBidsHistoryAPI,
    MyBidsListAPI,
    MyCheckoutListAPI,
    MyCompletedListAPI,
    MyLoadsHistoryAPI,
    MyLoadsListAPI,
    OrderCreateAPI,
    OrderDeleteAPI,
    OrderDetailAPI,
    OrderListAPI,
    OrderRefuseAPI,
    OrderUpdateAPI,
    assign,
    next_status,
    previous_status,
)

from apps.order.api.v1.apis.order_apis import MyLoadSet

app_name = "orders"

urlpatterns = [
    path("", OrderListAPI.as_view(), name="order-list"),
    path("create/", OrderCreateAPI.as_view(), name="order-create"),
    path("refuse/", OrderRefuseAPI.as_view(), name="order-refuse"),
    path("<int:pk>/", OrderDetailAPI.as_view(), name="order-detail"),
    path("<int:pk>/update/", OrderUpdateAPI.as_view(), name="order-update"),
    path("<int:pk>/delete/", OrderDeleteAPI.as_view(), name="order-delete"),
    path("last_similar/<int:pk>/", LastSimilarOrdersAPI.as_view(), name="last-similar-orders"),
]

# my bids
urlpatterns += [
    path("my_bids/", MyBidsListAPI.as_view(), name="my-bids-list"),
    path("my_bids/history/", MyBidsHistoryAPI.as_view(), name="my-bids-history"),
    path("my_bids/assign/", assign, name="my-bids-assign"),
    path("my_bids/my_load/", MyLoadSet.as_view(), name="my-bids-load"),
]

# my loads
urlpatterns += [
    path("my_loads/", MyLoadsListAPI.as_view(), name="my-loads"),
    path("my_loads/history/", MyLoadsHistoryAPI.as_view(), name="my-loads-history"),
    path("my_loads/checkout/", MyCheckoutListAPI.as_view(), name="my-checkouts"),
    path("my_loads/complete/", MyCompletedListAPI.as_view(), name="my-complete"),
    path("my_loads/next_status/", next_status, name="next-status"),
    path("my_loads/previous_status/", previous_status, name="previous-status"),
]
