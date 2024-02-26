from django.urls import path

from apps.letter.api.v1.apis import letter_apis

app_name = "letters"

urlpatterns = [
    path("", letter_apis.LetterListView.as_view(), name="letter-list"),
    path("<int:pk>/", letter_apis.LetterRetrieveDestroyView.as_view(), name="letter-list"),
    path("send/", letter_apis.SendEmailView.as_view(), name="send_email"),
]
