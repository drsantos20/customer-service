from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=50, null=True)
    phone = models.IntegerField(null=False)

    class Meta:
        db_table = 'user'
