from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.views import (
    ChangePasswordAPIView,
    CreatePinAPIView,
    LoginAPIView,
    LogoutAPIView,
    PinLoginAPIView,
    RegisterUserAPIView,
    RequestNewOTPAPIView,
    RequestPasswordResetAPIView,
    SetNewPasswordAPIView,
    VerifyEmailAPIView,
)

urlpatterns = [
    path("users/register/", RegisterUserAPIView.as_view(), name="register"),
    path("users/new-otp/", RequestNewOTPAPIView.as_view(), name="new_otp"),
    path(
        "users/email-verify/",
        VerifyEmailAPIView.as_view(),
        name="email_verify",
    ),
    path("users/login/", LoginAPIView.as_view(), name="login"),
    path("users/create-pin", CreatePinAPIView.as_view(), name="create_pin"),
    path("users/pin-login", PinLoginAPIView.as_view(), name="pin=login"),
    path(
        "users/request-password-reset/",
        RequestPasswordResetAPIView.as_view(),
        name="request_password_reset",
    ),
    path(
        "users/change-password/",
        ChangePasswordAPIView.as_view(),
        name="change_password",
    ),
    path(
        "users/password-reset-complete/",
        SetNewPasswordAPIView.as_view(),
        name="password_reset_complete",
    ),
    path("users/logout/", LogoutAPIView.as_view(), name="logout"),
    path(
        "users/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
