from django.urls import path, include
from .views import send_mail


urlpatterns = [
    path('order/<int:pk>/<int:rate>/', send_mail, name='send_mail'),
]
