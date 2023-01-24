from django.db import models

from apps.users.models import User
from apps.utility.base_model import TimeStampedUUIDModel


class Currency(TimeStampedUUIDModel):
    name = models.CharField(max_length=512, unique=True)
    currency_code = models.CharField(max_length=5, unique=True)

    def __str__(self) -> str:
        return f"{self.name} =====> {self.currency_code}"


class UserCurrency(TimeStampedUUIDModel):
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL)
    user = models.OneToOneField(User, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"{self.user} =====> {self.currency}"
