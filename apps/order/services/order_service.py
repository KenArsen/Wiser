from django.shortcuts import get_object_or_404
from geopy.distance import geodesic
from rest_framework import status
from rest_framework.exceptions import ValidationError

from apps.order.models import Order
from apps.order.repositories import OrderRepository


class OrderService:
    def __init__(self, serializer, repository=OrderRepository):
        self.serializer = serializer
        self.repository = repository

    def get_order(self, pk):
        return get_object_or_404(Order, pk=pk)

    def get_orders_by_status(self, status_):
        return self.repository.get_all_by_status(status_=status_)

    def get_orders(self):
        return self.repository.get_all()

    def create_order(self, data):
        serializer = self.serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            raise ValidationError(serializer.errors)

    def update_order(self, instance, data, partial=False):
        serializer = self.serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def delete_order(self, instance):
        if instance.user:
            instance.order_status = "EXPIRED"
            instance.save()
            return {"detail": "This order has been marked as inactive."}
        else:
            instance.delete()
            return {"detail": "Order deleted successfully."}

    def get_last_similar_orders(self, order_pk, radius=20, count=2):
        order = self.get_order(order_pk)
        order_my_bids = self.repository.get_all_by_status(status_="AWAITING_BID", order_by_="id")

        nearby_orders = []

        for bid in order_my_bids:
            distance_from = self._get_distance(order.coordinate_from, bid.coordinate_from)
            distance_to = self._get_distance(order.coordinate_to, bid.coordinate_to)

            if len(nearby_orders) >= count:
                break
            if distance_from <= radius and distance_to <= radius:
                nearby_orders.append(bid)

        serializer = self.serializer(nearby_orders, many=True)
        return {"nearby_orders": serializer.data}, status.HTTP_200_OK

    def _get_distance(self, coord1, coord2):
        lat1, lon1 = map(float, coord1.split(","))
        lat2, lon2 = map(float, coord2.split(","))
        distance = geodesic((lat1, lon1), (lat2, lon2)).km
        return distance
