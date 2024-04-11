from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, views
from rest_framework.response import Response

from apps.letter.api.v1.serializers.letter_serializer import (
    LetterReadSerializer,
    LetterWriteSerializer,
)
from apps.letter.models import Letter
from apps.letter.tasks import send_email


class LetterListAPI(generics.ListAPIView):
    queryset = Letter.objects.all()
    serializer_class = LetterReadSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class LetterDetailAPI(generics.RetrieveAPIView):
    queryset = Letter.objects.all()
    serializer_class = LetterReadSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class LetterDeleteAPI(generics.DestroyAPIView):
    queryset = Letter.objects.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class SendEmailView(views.APIView):
    @swagger_auto_schema(
        operation_summary="To send SMS",
        request_body=LetterWriteSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = LetterWriteSerializer(data=request.data)
        if serializer.is_valid():
            letter_instance = serializer.save()
            send_email.delay(letter_instance.id)
            return Response({"success": "Сообщение успешно отправлено"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
