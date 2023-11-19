from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.read_email import views
from api.views.read_email import OrderView, OrderFilterView

router = DefaultRouter()
router.register(r'orders', OrderView)

urlpatterns = [
    #path('read-email/', read_gmail, name='read-email'),
    path('orders/filter/', OrderFilterView.as_view(), name='order-filter'),
    path('', include(router.urls)),
]
