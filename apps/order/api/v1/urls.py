from django.urls import path

from apps.order.api.v1.apis import (
    GetDeliveryTime,
    GetLocationOrder,
    MyBidsDeleteAPI,
    MyBidsDetailAPI,
    MyBidsListAPI,
    MyBidsUpdateAPI,
    MyLoadsDeleteAPI,
    MyLoadsDetailAPI,
    MyLoadsListAPI,
    MyLoadsStatus,
    MyLoadsUpdateAPI,
    OrderCreateAPI,
    OrderDeleteAPI,
    OrderDetailAPI,
    OrderFilterView,
    OrderHistoryDeleteAPI,
    OrderHistoryDetailView,
    OrderHistoryListAPI,
    OrderHistoryUpdateView,
    OrderListAPI,
    OrderUpdateAPI,
    my_bids_no,
    my_bids_yes,
)

app_name = "orders"

urlpatterns = [
    path("", OrderListAPI.as_view(), name="order-list"),
    path("create/", OrderCreateAPI.as_view(), name="order-create"),
    path("<int:pk>/", OrderDetailAPI.as_view(), name="order-detail"),
    path("<int:pk>/update/", OrderUpdateAPI.as_view(), name="order-update"),
    path("<int:pk>/delete/", OrderDeleteAPI.as_view(), name="order-delete"),
    path("<int:pk>/delivery-time/", GetDeliveryTime.as_view(), name="order-delivery-time"),
    path("<int:pk>/location-order/", GetLocationOrder.as_view(), name="order-location"),
    path("filter/", OrderFilterView.as_view(), name="order-filter"),
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
    path("my_loads_status/<int:pk>/", MyLoadsStatus.as_view(), name="my-loads-status"),
]
