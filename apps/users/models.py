from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.dependencies.constants import AUTH_PROVIDER_CHOICES, EMAIL
from apps.users.managers import UserManager
from apps.utility.base_model import TimeStampedUUIDModel


class User(AbstractUser, TimeStampedUUIDModel):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="""Phone number must be entered in the format:
        '+999999999'. Up to 15 digits allowed.""",
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    is_verified = models.BooleanField(_("is email verified"), default=False)
    auth_provider = models.CharField(
        max_length=8, choices=AUTH_PROVIDER_CHOICES, default=EMAIL
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        indexes = [models.Index(fields=["email"], name="email_index")]

    def __str__(self):
        return f"{self.email}"

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}


class UserOTP(TimeStampedUUIDModel):
    otp = models.PositiveIntegerField()
    user = models.OneToOneField(User, on_delete=models.RESTRICT)

    class Meta:
        indexes = [models.Index(fields=["user"], name="otp_index")]

    def __str__(self):
        return f"{self.user.email} =====> {self.pin}"


class UserPin(TimeStampedUUIDModel):
    pin = models.CharField(max_length=256)
    user = models.OneToOneField(User, on_delete=models.RESTRICT)

    class Meta:
        indexes = [models.Index(fields=["user"], name="pin_index")]

    def __str__(self):
        return f"{self.user.email} =====> {self.pin}"
