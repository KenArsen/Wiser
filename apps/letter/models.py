from django.db import models


class Letter(models.Model):
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.comment[:30]}... '
