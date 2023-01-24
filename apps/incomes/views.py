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

from apps.incomes.filters import IncomeFilter
from apps.incomes.models import Income, IncomeType
from apps.incomes.serializers import IncomeSerializer, IncomeTypeSerializer
from apps.utility.permissions import IsOwner


class IncomeTypeViewset(ModelViewSet):
    queryset = IncomeType.objects.all()
    serializer_class = IncomeTypeSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = "id"

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return IncomeType.objects.none()
        return self.queryset.filter(user=self.request.user).select_related()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IncomeViewset(ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IncomeFilter
    lookup_field = "id"

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Income.objects.none()
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


class IncomeStatisticsView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        "date": ["lte", "gte"],
    }

    def return_date_range_income(self, start_date, end_date):

        income_types = (
            IncomeType.objects.filter(user=self.request.user)
            .select_related("user")
            .values_list("pkid", "name")
        )
        total_income = (
            Income.objects.filter(
                user=self.request.user,
                date__in=[start_date, end_date],
            )
            .select_related("user", "income_type")
            .aggregate(Sum("amount"))["amount__sum"]
        )

        income_dict = {}
        for income_type in income_types:
            income_dict[income_type[1]] = (
                Income.objects.filter(
                    income_type=income_type[0],
                    user=self.request.user,
                    date__in=[start_date, end_date],
                )
                .select_related("user", "income_type")
                .aggregate(Sum("amount"))["amount__sum"]
            )

            income_dict[income_type[1]] = (
                (
                    Income.objects.filter(
                        income_type=income_type[0],
                        user=self.request.user,
                        date__in=[start_date, end_date],
                    )
                    .select_related("user", "income_type")
                    .aggregate(Sum("amount"))["amount__sum"]
                )
                / total_income
                * 100
            )

        return income_dict

    def return_all_income(self):

        income_types = (
            IncomeType.objects.filter(user=self.request.user)
            .select_related("user")
            .values_list("pkid", "name")
        )

        total_income = (
            Income.objects.filter(
                user=self.request.user,
            )
            .select_related("user", "income_type")
            .aggregate(Sum("amount"))["amount__sum"]
        )

        income_dict = {}
        for income_type in income_types:
            income_data = (
                Income.objects.filter(
                    income_type=income_type[0],
                    user=self.request.user,
                )
                .select_related("user", "income_type")
                .aggregate(Sum("amount"))["amount__sum"]
            )

            income_dict[income_type[1]] = income_data

            income_data = (
                (
                    Income.objects.filter(
                        income_type=income_type[0],
                        user=self.request.user,
                    )
                    .select_related("user", "income_type")
                    .aggregate(Sum("amount"))["amount__sum"]
                )
                / total_income
                * 100
            )

            income_dict[income_type[1]] = income_data

        return income_dict

    @swagger_auto_schema(manual_parameters=[date__lte_param, date__gte_param])
    def get(self, request):
        start_date = self.request.query_params.get("date__gte")
        end_date = self.request.query_params.get("date__lte")

        if not start_date or end_date:
            return Response(self.return_all_income(), status=status.HTTP_200_OK)

        return Response(
            self.return_date_range_income(start_date=start_date, end_date=end_date),
            status=status.HTTP_200_OK,
        )
