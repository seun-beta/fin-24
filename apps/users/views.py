from rest_framework import generics, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.serializers import (
    ChangePasswordSerializer,
    CreatePinSerializer,
    LoginSerializer,
    LogoutSerializer,
    PinLoginSerializer,
    RegisterUserSerializer,
    RequestNewOTPSerializer,
    RequestPasswordResetSerializer,
    SetNewPasswordSerializer,
    VerifyEmailSerializer,
)


class RegisterUserAPIView(GenericAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RequestNewOTPAPIView(GenericAPIView):
    serializer_class = RequestNewOTPSerializer
    permission_classes = []

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"data": "OTP sent to email address successfully"},
            status=status.HTTP_200_OK,
        )


class VerifyEmailAPIView(GenericAPIView):
    serializer_class = VerifyEmailSerializer
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"data": "email has been verified successfully"},
            status=status.HTTP_200_OK,
        )


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreatePinAPIView(GenericAPIView):
    serializer_class = CreatePinSerializer
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PinLoginAPIView(generics.GenericAPIView):
    serializer_class = PinLoginSerializer
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetAPIView(GenericAPIView):
    serializer_class = RequestPasswordResetSerializer
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"data": "We have sent you a link to reset your password"},
            status=status.HTTP_200_OK,
        )


class ChangePasswordAPIView(GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = request.user

        return Response(
            {"data": user.tokens()},
            status=status.HTTP_200_OK,
        )


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": serializer.validated_data}, status=status.HTTP_200_OK)


class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
