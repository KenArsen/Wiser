from django.urls import path

from apps.read_email.parser import read_gmail

urlpatterns = [
    path('read-emails/', read_gmail),
]
