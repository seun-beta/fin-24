# from django.db.models import Sum

# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.generics import ListAPIView
# from rest_framework.viewsets import ModelViewSet

# from apps.expenses.models import Expense
# from apps.expenses.serializers import ExpenseSerializer, ExpenseStatisticsSerializer


# class ExpenseViewset(ModelViewSet):
#     queryset = Expense.objects.all()
#     serializer_class = ExpenseSerializer

#     def get_queryset(self):
#         return self.queryset.filter(user=self.request.user).select_related()


# class ExpenseStatistics(ListAPIView):
#     queryset = Expense.objects.all()
#     serializer_class = ExpenseStatisticsSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ["expense_type", "account_type"]

#     def get_queryset(self):
#         return self.queryset.filter(user=self.request.user).aggregate(Sum("amount"))


from django.db.models import Sum

from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.expenses.filters import ExpenseFilter
from apps.expenses.models import Expense, ExpenseType
from apps.expenses.serializers import ExpenseSerializer, ExpenseTypeSerializer
from apps.utility.permissions import IsOwner


class ExpenseTypeViewset(ModelViewSet):
    queryset = ExpenseType.objects.all()
    serializer_class = ExpenseTypeSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = "id"

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return ExpenseType.objects.none()
        return self.queryset.filter(user=self.request.user).select_related()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseViewset(ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExpenseFilter
    lookup_field = "id"

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Expense.objects.none()
        return self.queryset.filter(user=self.request.user).select_related()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


date__lte_param = openapi.Parameter(
    "date__lte",
    openapi.IN_QUERY,
    description="date__lte",
    type=openapi.TYPE_STRING,
)
date__gte_param = openapi.Parameter(
    "date__gte",
    openapi.IN_QUERY,
    description="date__gte",
    type=openapi.TYPE_STRING,
)


class ExpenseStatisticsView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "date": ["lte", "gte"],
    }

    def return_date_range_expense(self, start_date, end_date):

        expense_types = (
            ExpenseType.objects.filter(user=self.request.user)
            .select_related("user")
            .values_list("pkid", "name")
        )
        total_expense = (
            Expense.objects.filter(
                user=self.request.user,
                date__in=[start_date, end_date],
            )
            .select_related("user", "expense_type")
            .aggregate(Sum("amount"))["amount__sum"]
        )

        expense_dict = {}
        for expense_type in expense_types:
            expense_dict[expense_type[1]] = (
                Expense.objects.filter(
                    expense_type=expense_type[0],
                    user=self.request.user,
                    date__in=[start_date, end_date],
                )
                .select_related("user", "expense_type")
                .aggregate(Sum("amount"))["amount__sum"]
            )

            expense_dict[expense_type[1]] = (
                (
                    Expense.objects.filter(
                        expense_type=expense_type[0],
                        user=self.request.user,
                        date__in=[start_date, end_date],
                    )
                    .select_related("user", "expense_type")
                    .aggregate(Sum("amount"))["amount__sum"]
                )
                / total_expense
                * 100
            )

        return expense_dict

    def return_all_expense(self):

        expense_types = (
            ExpenseType.objects.filter(user=self.request.user)
            .select_related("user")
            .values_list("pkid", "name")
        )

        total_expense = (
            Expense.objects.filter(
                user=self.request.user,
            )
            .select_related("user", "expense_type")
            .aggregate(Sum("amount"))["amount__sum"]
        )

        expense_dict = {}
        for expense_type in expense_types:
            expense_data = (
                Expense.objects.filter(
                    expense_type=expense_type[0],
                    user=self.request.user,
                )
                .select_related("user", "expense_type")
                .aggregate(Sum("amount"))["amount__sum"]
            )

            expense_dict[expense_type[1]] = expense_data

            expense_data = (
                (
                    Expense.objects.filter(
                        expense_type=expense_type[0],
                        user=self.request.user,
                    )
                    .select_related("user", "expense_type")
                    .aggregate(Sum("amount"))["amount__sum"]
                )
                / total_expense
                * 100
            )

            expense_dict[expense_type[1]] = expense_data

        return expense_dict

    @swagger_auto_schema(manual_parameters=[date__lte_param, date__gte_param])
    def get(self, request):
        start_date = self.request.query_params.get("date__gte")
        end_date = self.request.query_params.get("date__lte")

        if not start_date or end_date:
            return Response(self.return_all_expense(), status=status.HTTP_200_OK)

        return Response(
            self.return_date_range_expense(start_date=start_date, end_date=end_date),
            status=status.HTTP_200_OK,
        )
