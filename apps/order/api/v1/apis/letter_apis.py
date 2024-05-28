import logging
from smtplib import SMTPAuthenticationError, SMTPException

from django.conf import settings
from django.core.mail import send_mail
from rest_framework.exceptions import ValidationError

from drf_yasg.utils import swagger_auto_schema
from rest_framework import exceptions, generics, status, views
from rest_framework.response import Response

from apps.order.models import Order, Letter
from apps.order.api.v1.serializers import LetterSerializer


def send_email(data):
    try:
        logging.info(f"***** Sending email for letter {data['id']} *****")
        order = Order.objects.get(id=data["order"])
        order.status = "AWAITING_BID"
        order.save()
        if order.broker_email:
            subject = "New comment added"
            message = "A new comment has been added:\n\n"
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=["arsen.kenjegulov.bj@gmail.com", "alymbekjenishbekuulu@gmail.com"],
                fail_silently=False,
                html_message=data["comment"],
            )
            logging.info(f"***** Email to {order.broker_email} sent successfully *****")
    except Order.DoesNotExist:
        raise ValidationError({"detail": "No such order found"})
    except (SMTPAuthenticationError, SMTPException) as e:
        raise ValidationError({"error", f"{e}"})
    except Exception as e:
        raise ValidationError({"error": f"{e}"})


class SendEmailView(views.APIView):
    @swagger_auto_schema(
        operation_summary="To send SMS",
        request_body=LetterSerializer,
    )
    def post(self, request, *args, **kwargs):
        try:
            order_id = request.data.get("order")
            if not order_id:
                raise exceptions.ValidationError({"detail": "order is required"})
            order = Order.objects.get(id=order_id)
            if hasattr(order, "letter"):
                order.letter.delete()
        except Order.DoesNotExist:
            raise exceptions.ValidationError({"detail": "Order does not exist"})

        serializer = LetterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_email(serializer.data)
            return Response({"success": "Message sent successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
