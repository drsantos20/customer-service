from django.db import models

from api.order.models import Address


class Order(models.Model):
    user = models.ForeignKey('order.User', on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    class Meta:
        db_table = 'order'
