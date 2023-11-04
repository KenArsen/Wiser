from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.read_email.parser import read_gmail
from api.views.read_email import OrderView

router = DefaultRouter()
router.register(r'orders', OrderView)

urlpatterns = [
    path('read-email/', read_gmail, name='read-email'),
    path('', include(router.urls)),
]
