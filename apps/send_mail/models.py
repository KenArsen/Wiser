from django.db import models


class Letter(models.Model):
    rate = models.IntegerField(blank=True, null=True)
    dims = models.CharField(max_length=255, blank=True, null=True)
    mc = models.CharField(max_length=255, blank=True, null=True)
    miles = models.FloatField(blank=True, null=True)
    eta_to_pick_up = models.CharField(max_length=255, blank=True, null=True)
    dock_high = models.BooleanField(blank=True, null=True)
    account = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f'{self.rate} ...'
