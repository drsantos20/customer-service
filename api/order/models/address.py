from django.db import models


class UserOrderAddress(models.Model):
    street = models.CharField(max_length=150, null=False, blank=False)
    city = models.CharField(max_length=150, null=False, blank=False)
    neighborhood = models.CharField(max_length=150, null=False, blank=False)
    zip_code = models.CharField(max_length=12)
    uf = models.CharField(max_length=12)
