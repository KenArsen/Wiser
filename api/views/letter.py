from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.letter.models import Letter
from api.serializers.letter import LetterSerializer
from apps.letter.tasks import send_email


class LetterListView(generics.ListAPIView):
    queryset = Letter.objects.all()
    serializer_class = LetterSerializer


class LetterRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    queryset = Letter.objects.all()
    serializer_class = LetterSerializer


class SendEmailView(APIView):
    @swagger_auto_schema(
        operation_summary="To send SMS",
        request_body=LetterSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = LetterSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.validated_data['comment']
            serializer.save()
            send_email(comment)
            return Response({'success': 'Сообщение успешно отправлено'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
