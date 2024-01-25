from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from rest_framework import status
from rest_framework.response import Response

from apps.read_email.models import Order
from .models import Letter
from .serializers import LetterSerializer


def send_mail(request, pk, rate):
    letter = Letter()
    try:
        order = Order.objects.get(pk=pk)
        letter.rate = rate
        letter.dims = order.dims
        letter.mc = '1220386'
        letter.miles_out = order.miles
        letter.eta_to_pick_up = get_delivery_time(order)
        letter.dock_high = True
        letter.account = order.from_whom

        serializer = LetterSerializer(data=letter.__dict__)

        if serializer.is_valid():
            serializer.save()

            email_body = render_to_string('send_email.html', {'letter': letter})
            email = EmailMultiAlternatives(
                subject='',
                body=strip_tags(email_body),
                from_email=settings.EMAIL_HOST_USER,
                to=['tan.me4nik@gmail.com']
            )
            email.attach_alternative(email_body, 'text/html')
            email.send()
            return Response({"message": "Mail sent successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)


def get_delivery_time(order):
    delivery_time = order.deliver_date_EST if order.is_active else None

    if delivery_time is None:
        return {"error": "Delivery time not specified or order is not active."}

    current_time = timezone.localtime(timezone.now())

    time_until_delivery = delivery_time - current_time

    total_seconds = time_until_delivery.total_seconds()

    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, _ = divmod(remainder, 60)

    hours += days * 24

    return f"{int(hours)}:{int(minutes)}"
