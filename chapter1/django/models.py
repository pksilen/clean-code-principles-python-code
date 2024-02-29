from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class SalesItem(models.Model):
    user_account_id = models.BigIntegerField()
    name = models.CharField(max_length=512)
    price = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(2147483647)]
    )
