from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Letter
from .serializers import LetterSerializer
from .tasks import send_email


class LetterListView(generics.ListAPIView):
    queryset = Letter.objects.all()
    serializer_class = LetterSerializer


class LetterRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Letter.objects.all()
    serializer_class = LetterSerializer


class SendEmailView(APIView):
    def post(self, request, *args, **kwargs):
        comment = request.data.get('comment', '')

        # Отправка письма
        send_email(comment)
        return Response({'success': 'Сообщение успешно отправлено'}, status=status.HTTP_200_OK)
