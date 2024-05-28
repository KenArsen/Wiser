from django.urls import path

from apps.order.api.v1.apis import (
    SendEmailView,
    LoadBoardDetailAPI,
    LoadBoardListAPI,
    MyBidHistoryAPI,
    MyBidListAPI,
    MyCheckoutListAPI,
    MyCompletedListAPI,
    MyLoadHistoryAPI,
    MyLoadListAPI,
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

app_name = "orders"

urlpatterns = [
    path("list/", OrderListAPI.as_view(), name="order-list"),
    path("create/", OrderCreateAPI.as_view(), name="order-create"),
    path("refuse/", OrderRefuseAPI.as_view(), name="order-refuse"),
    path("<int:pk>/", OrderDetailAPI.as_view(), name="order-detail"),
    path("<int:pk>/update/", OrderUpdateAPI.as_view(), name="order-update"),
    path("<int:pk>/delete/", OrderDeleteAPI.as_view(), name="order-delete"),
]

# load board
urlpatterns += [
    path("load_boards/", LoadBoardListAPI.as_view(), name="load-board-list"),
    path(
        "load_boards/<int:pk>/", LoadBoardDetailAPI.as_view(), name="load-board-detail"
    ),
    path("send/", SendEmailView.as_view(), name="send-email"),
]

# my bids
urlpatterns += [
    path("my_bids/", MyBidListAPI.as_view(), name="my-bids-list"),
    path("my_bids/history/", MyBidHistoryAPI.as_view(), name="my-bids-history"),
    path("my_bids/assign/", assign, name="my-bids-assign"),
]

# my loads
urlpatterns += [
    path("my_loads/", MyLoadListAPI.as_view(), name="my-loads"),
    path("my_loads/history/", MyLoadHistoryAPI.as_view(), name="my-loads-history"),
    path("my_loads/checkout/", MyCheckoutListAPI.as_view(), name="my-checkouts"),
    path("my_loads/complete/", MyCompletedListAPI.as_view(), name="my-complete"),
    path("my_loads/next_status/", next_status, name="next-status"),
    path("my_loads/previous_status/", previous_status, name="previous-status"),
]
