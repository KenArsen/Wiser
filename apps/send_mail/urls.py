from django.urls import path, include
from .views import send_mail


urlpatterns = [
    path('order/<int:order_id>/<int:driver_id>/<int:rate>/', send_mail, name='send_mail'),
]
