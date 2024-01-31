from django.urls import path, include
from rest_framework import routers

from .views import send_mail, LetterViewSet

router = routers.DefaultRouter()
router.register(r'', LetterViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('send/<int:order_id>/<int:driver_id>/<int:rate>/', send_mail, name='send_mail'),
]
