from django.db import models

from apps.users.models import User
from apps.utility.base_model import TimeStampedUUIDModel


class IncomeType(TimeStampedUUIDModel):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.name} =====> {self.user}"


class Income(TimeStampedUUIDModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    note = models.CharField(max_length=512, null=True, blank=True)
    description = models.CharField(max_length=1024, null=True, blank=True)
    image = models.URLField()
    income_type = models.ForeignKey(IncomeType, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.id}   {self.amount} =====> {self.income_type.name}"
