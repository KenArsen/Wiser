from django.db import models

from apps.user.models import User


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    from_whom = models.EmailField(null=True, blank=True)

    pick_up_at = models.CharField(max_length=255, blank=True, null=True)

    pick_up_date_CEN = models.DateTimeField(blank=True, null=True)
    pick_up_date_EST = models.DateTimeField(blank=True, null=True)

    deliver_to = models.CharField(max_length=255, blank=True, null=True)
    deliver_date_CEN = models.DateTimeField(blank=True, null=True)
    deliver_date_EST = models.DateTimeField(blank=True, null=True)

    notes = models.CharField(max_length=400, blank=True, null=True)
    miles = models.FloatField(blank=True, null=True)
    pieces = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    dims = models.CharField(max_length=255, blank=True, null=True)

    stackable = models.CharField(max_length=255, blank=True, null=True)
    hazardous = models.CharField(max_length=255, blank=True, null=True)
    fast_load = models.CharField(max_length=255, blank=True, null=True)
    dock_level = models.CharField(max_length=255, blank=True, null=True)

    suggested_truck_size = models.CharField(max_length=255, blank=True, null=True)

    this_posting_expires_cen = models.DateTimeField(blank=True, null=True)
    this_posting_expires_est = models.DateTimeField(blank=True, null=True)

    load_posted_by = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    order_number = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.from_whom
