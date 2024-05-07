from geopy.distance import geodesic
from rest_framework import status

from apps.order.repositories import OrderRepository


class LastSimilarService:
    def __init__(self, serializer, repository=OrderRepository):
        self.serializer = serializer
        self.repository = repository

    def get_last_similar_orders(self, order_pk, radius=20, count=2):
        order = self.repository.get_order(pk=order_pk)
        order_my_bids = self.repository.get_orders_by_status(status_="AWAITING_BID", order_by_="-id")

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
