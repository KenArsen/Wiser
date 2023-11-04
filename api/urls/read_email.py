from django.urls import path

from apps.read_email.parser import read_gmail
from api.views.read_email import OrderView

urlpatterns = [
    path('read-email/', read_gmail),
    path('', OrderView.as_view()),
]
