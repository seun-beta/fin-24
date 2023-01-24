from rest_framework import serializers

from apps.commons.models import Currency, UserCurrency


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        exclude = ["created_at", "updated_at"]


class UserCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCurrency
        exclude = ["created_at", "updated_at", "user"]


class MonoAuthTokenSeralizer(serializers.Serializer):
    auth_token = serializers.CharField()


class MonoWebHookSerializer(serializers.Serializer):
    data = serializers.JSONField()
