from django.contrib import admin

from apps.incomes.models import Income, IncomeType

admin.site.register(Income)
admin.site.register(IncomeType)
