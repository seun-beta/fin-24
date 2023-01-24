from django.urls import path

from rest_framework.routers import SimpleRouter

from apps.expenses.views import (
    ExpenseStatisticsView,
    ExpenseTypeViewset,
    ExpenseViewset,
)

router = SimpleRouter()

urlpatterns = [
    path(
        "expenses/expense-statistics",
        ExpenseStatisticsView.as_view(),
        name="expense_statistics",
    )
]
router.register(r"expense-type", ExpenseTypeViewset, basename="expense_type")
router.register(r"expenses", ExpenseViewset, basename="expense")
