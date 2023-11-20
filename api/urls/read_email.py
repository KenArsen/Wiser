from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views.read_email import OrderView, OrderFilterView

router = DefaultRouter()
router.register(r'orders', OrderView)

urlpatterns = [
    path('orders/filter/', OrderFilterView.as_view(), name='order-filter'),
    path('', include(router.urls)),
]
