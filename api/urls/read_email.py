from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views.read_email import OrderView, OrderFilterView, OrderHistoryView, delete_all_orders

router = DefaultRouter()
router.register(r'orders', OrderView)
router.register(r'order-history', OrderHistoryView, basename='orderhistory')

urlpatterns = [
    path('orders/delete/all/', delete_all_orders),
    path('orders/filter/', OrderFilterView.as_view(), name='order-filter'),
    path('orders/<int:pk>/delivery-time/', OrderView.as_view({'get': 'get_delivery_time'}), name='order-delivery-time'),
    path('orders/<int:pk>/location-order/',
         OrderView.as_view({'get': 'get_location_order', 'post': 'get_location_order'}), name='order-location'),

    path('', include(router.urls)),
]
