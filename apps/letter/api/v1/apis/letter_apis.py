from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views
from rest_framework.response import Response

from apps.letter.api.v1.serializers.letter_serializer import (
    LetterDetailSerializer,
    LetterSerializer,
)
from apps.letter.models import Letter
from apps.letter.tasks import send_email


class LetterListAPI(views.APIView):
    def get(self, request):
        queryset = Letter.objects.all()
        serializer = LetterSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LetterDetailAPI(views.APIView):
    def get(self, request, pk):
        letter = get_object_or_404(Letter, pk=pk)
        serializer = LetterSerializer(letter)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LetterDeleteAPI(views.APIView):
    def delete(self, request, pk):
        letter = get_object_or_404(Letter, pk=pk)
        letter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SendEmailView(views.APIView):
    @swagger_auto_schema(
        operation_summary="To send SMS",
        request_body=LetterDetailSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = LetterDetailSerializer(data=request.data)
        if serializer.is_valid():
            letter_instance = serializer.save()
            send_email.delay(letter_instance.id)
            return Response({"success": "Сообщение успешно отправлено"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
