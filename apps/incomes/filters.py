import django_filters as filters

from apps.incomes.models import Income


class IncomeFilter(filters.FilterSet):
    amount = filters.CharFilter(field_name="amount", lookup_expr="icontains")
    note = filters.CharFilter(field_name="note", lookup_expr="icontains")
    description = filters.CharFilter(field_name="description", lookup_expr="icontains")
    start_date = filters.DateFilter(field_name="date", lookup_expr="gte")
    end_date = filters.DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = Income
        fields = [
            "amount",
            "note",
            "description",
            "start_date",
            "end_date",
        ]
