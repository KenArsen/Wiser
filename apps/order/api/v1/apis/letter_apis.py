import logging
from smtplib import SMTPAuthenticationError, SMTPException

from django.conf import settings
from django.core.mail import send_mail
from rest_framework import exceptions, generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.common.permissions import HasAccessToMyBidsPanel
from apps.order.api.v1.serializers import LetterSerializer
from apps.order.models import Order


def send_email(data):
    try:
        logging.info(f"***** Sending email for letter {data['id']} *****")
        order = Order.objects.get(id=data["order"])
        order.status = "AWAITING_BID"
        order.save(update_fields=["status"])
        if order.broker_email:
            subject = "New comment added"
            message = "A new comment has been added:\n\n"
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[order.broker_email],
                fail_silently=False,
                html_message=data["comment"],
            )
            logging.info(f"***** Email to {order.broker_email} sent successfully *****")
        else:
            logging.warning(f"No email address found for order {order.id}")
    except Order.DoesNotExist:
        raise ValidationError({"detail": "No such order found"})
    except (SMTPAuthenticationError, SMTPException) as e:
        raise ValidationError({"error": str(e)})
    except Exception as e:
        raise ValidationError({"error": str(e)})


class SendEmailView(generics.GenericAPIView):
    serializer_class = LetterSerializer
    permission_classes = (HasAccessToMyBidsPanel,)

    @staticmethod
    def delete_existing_letter(order_id):
        try:
            order = Order.objects.get(id=order_id)
            if hasattr(order, "letter"):
                order.letter.delete()
        except Order.DoesNotExist:
            raise exceptions.ValidationError({"detail": "Order does not exist"})

    def post(self, request, *args, **kwargs):
        order_id = request.data.get("order")
        if not order_id:
            raise exceptions.ValidationError({"detail": "Order ID is required"})

        self.delete_existing_letter(order_id)

        serializer = LetterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            order = Order.objects.get(id=order_id)
            order.user = request.user
            order.save()
            send_email(serializer.data)
            return Response({"success": "Message sent successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
