from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets

from api.utils.permissions import IsDispatcher, IsAdmin
from apps.read_email.models import Order
from .models import Letter
from .serializers import LetterSerializer
from .tasks import send_mail_to_order


class LetterViewSet(viewsets.ModelViewSet):
    queryset = Letter.objects.all()
    serializer_class = LetterSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdmin | IsDispatcher])
@action(methods=["GET"], detail=False)
def send_mail(request, order_id, driver_id, rate):
    order = get_object_or_404(Order, pk=order_id)

    letter = create_letter(order, rate)
    serializer = LetterSerializer(data=letter.__dict__)

    if serializer.is_valid():
        serializer.save()
        send_mail_to_order.delay(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def create_letter(order, rate):
    letter = Letter()
    letter.rate = rate
    letter.dims = order.dims
    letter.mc = '1220386'
    letter.miles = order.miles
    letter.eta_to_pick_up = get_delivery_time(order)
    letter.dock_high = True
    letter.account = order.from_whom
    return letter


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
