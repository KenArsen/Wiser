from django.urls import path

from apps.letter.api.v1.apis.letter import (
    LetterListView,
    LetterRetrieveDestroyView,
    SendEmailView,
)

app_name = "letter"

urlpatterns = [
    path("", LetterListView.as_view(), name="letter-list"),
    path("<int:pk>/", LetterRetrieveDestroyView.as_view(), name="letter-list"),
    path("send/", SendEmailView.as_view(), name="send_email"),
]
