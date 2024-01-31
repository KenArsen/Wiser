from django.urls import path

from .views import LetterRetrieveDestroyView, LetterListView, SendEmailView

urlpatterns = [
    path('', LetterListView.as_view(), name='letter-list'),
    path('<int:pk>/', LetterRetrieveDestroyView.as_view(), name='letter-list'),
    path('send/', SendEmailView.as_view(), name='send_email'),
]
