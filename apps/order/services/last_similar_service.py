from math import asin, cos, radians, sin, sqrt

from rest_framework import status

from apps.order.repositories import OrderRepository


class LastSimilarService:
    def __init__(self, serializer, repository=OrderRepository):
        self.serializer = serializer
        self.repository = repository

    def get_last_similar_orders(self, order_pk, radius=20):
        order = self.repository.get_order(pk=order_pk)
        order_my_bids = self.repository.get_filtered_orders(order_status="COMPLETED")

        nearby_orders = []

        for bid in order_my_bids:
            distance_from = self._get_distance(order.coordinate_from, bid.coordinate_from)
            distance_to = self._get_distance(order.coordinate_to, bid.coordinate_to)

            if distance_from <= radius and distance_to <= radius:
                nearby_orders.append(bid)

        serializer = self.serializer(nearby_orders, many=True)
        return {"nearby_orders": serializer.data}, status.HTTP_200_OK

    def _get_distance(self, coord1, coord2):
        lat1, lon1 = map(float, coord1.split(","))
        lat2, lon2 = map(float, coord2.split(","))
        distance = self.distance(lat1, lat2, lon1, lon2)
        return distance

    @staticmethod
    def distance(lat1, lat2, lon1, lon2):
        lon1 = radians(lon1)
        lon2 = radians(lon2)
        lat1 = radians(lat1)
        lat2 = radians(lat2)

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))

        r = 6371

        return c * r
