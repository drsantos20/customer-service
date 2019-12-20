from django.db import models

from api.order.models import UserOrderAddress


class UserOrder(models.Model):
    user = models.ForeignKey('order.User', on_delete=models.CASCADE)
    address = models.ForeignKey(UserOrderAddress, on_delete=models.CASCADE)

    class Meta:
        db_table = 'order'
