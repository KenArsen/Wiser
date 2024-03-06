from django.urls import path

from apps.order.api.v1.apis import (
    GetDeliveryTime,
    GetLocationOrder,
    MyBidsListAPI,
    MyLoadsListAPI,
    MyLoadsStatus,
    OrderCreateAPI,
    OrderDeleteAPI,
    OrderDetailAPI,
    OrderFilterView,
    OrderHistoryListAPI,
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
]

# my bids
urlpatterns += [
    path("my_bids/", MyBidsListAPI.as_view(), name="my-bids-list"),
    path("my_bids/<int:pk>/yes/", my_bids_yes, name="my-bids-yes"),
    path("my_bids/<int:pk>/no/", my_bids_no, name="my-bids-no"),
]

# my loads
urlpatterns += [
    path("my_loads/", MyLoadsListAPI.as_view(), name="my-loads"),
    path("my_loads_status/<int:pk>/", MyLoadsStatus.as_view(), name="my-loads-status"),
]
