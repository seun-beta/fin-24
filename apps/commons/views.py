from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.commons.models import Currency, UserCurrency
from apps.commons.serializers import (
    CurrencySerializer,
    MonoAuthTokenSeralizer,
    UserCurrencySerializer,
)
from apps.commons.services.account_id_service import get_account_id
from apps.utility.permissions import IsOwner


class CurrencyView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class UserCurrencyViewset(ModelViewSet):
    queryset = UserCurrency.objects.all()
    serializer_class = UserCurrencySerializer
    permission_classes = [IsAuthenticated, IsOwner]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).select_related()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MonoAuthTokenView(GenericAPIView):
    serializer_class = MonoAuthTokenSeralizer

    def post(self, request) -> Response:
        auth_token = self.serializer_class(data=request.data)
        get_account_id(auth_token=auth_token)
        return Response("account id successfully retrievec", status=status.HTTP_200_OK)


class MonoWebHookView(APIView):
    def post(self, request):
        """
                {
          event: 'mono.events.account_updated',
          data: {
            meta: {
              data_status: 'AVAILABLE',
              auth_method: 'mobile_banking'//internet_banking
            },
            account: {
              _id: '5fbcde8f8699984153e65537',
              institution: {
                "name": "GTBank",
                "bankCode": "058",
                "type": "PERSONAL_BANKING"
              },
              accountNumber: '0018709596',
              name: 'OGUNGBEFUN OLADUNNI KHADIJAH',
              type: 'SAVINGS_ACCOUNT',
              currency: 'Naira',
              bvn: '9422',
              balance: 3033984,
              created_at: '2020-11-24T10:21:03.936Z',
              updated_at: '2020-11-24T10:21:13.050Z',
              __v: 0
            }
          }
        }
        """

        data = self.request

        if data["event"] == "mono.events.account_updated":
            pass
