from django.urls import path

from apps.letter.api.v1.apis import (
    LetterDeleteAPI,
    LetterDetailAPI,
    LetterListAPI,
    SendEmailView,
)

app_name = "letters"

urlpatterns = [
    path("", LetterListAPI.as_view(), name="letter-list"),
    path("<int:pk>/", LetterDetailAPI.as_view(), name="letter-list"),
    path("<int:pk>/delete/", LetterDeleteAPI.as_view(), name="letter-delete"),
    path("send/", SendEmailView.as_view(), name="send_email"),
]
