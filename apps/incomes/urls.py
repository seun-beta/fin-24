from django.urls import path

from rest_framework.routers import SimpleRouter

from apps.incomes.views import IncomeStatisticsView, IncomeTypeViewset, IncomeViewset

router = SimpleRouter()

urlpatterns = [
    path(
        "incomes/income-statistics",
        IncomeStatisticsView.as_view(),
        name="income_statistics",
    )
]
router.register(r"income-type", IncomeTypeViewset, basename="income_type")
router.register(r"incomes", IncomeViewset, basename="income")
