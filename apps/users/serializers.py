import django.contrib.auth.password_validation as validators
from django.contrib import auth
from django.core import exceptions
from django.db.transaction import atomic

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from apps.users.models import User, UserOTP, UserPin
from apps.users.tasks import (
    send_account_activation_email,
    send_new_otp_email,
    send_password_reset_otp_email,
)
from apps.utility.hasher_util import hash_pin, verify_pin
from apps.utility.otp_generator import generate_otp


class RegisterUserSerializer(serializers.ModelSerializer):

    """Serializer for user registration by email
    and initial One-Time-Password(OTP) generation"""

    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "password",
            "password2",
            "email",
            "phone_number",
            "first_name",
            "last_name",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "phone_number": {"required": True},
        }

    def validate(self, attrs) -> User:
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("Passwords do not match")
        try:
            validators.validate_password(password=attrs["password"])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(str(e))
        return attrs

    @atomic
    def create(self, validated_data) -> User:
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        user_otp = UserOTP.objects.create(user=user, otp=generate_otp())
        send_account_activation_email.delay(user.email, user_otp.otp, user.first_name)

        return user


class RequestNewOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2, max_length=100)

    def validate(self, attrs) -> dict:
        email = attrs.get("email", "")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("user does not exist")
        if user.is_verified:
            raise serializers.ValidationError("email is already verified")

        return attrs

    def create(self, validated_data) -> dict:
        user = User.objects.get(email=validated_data["email"])
        UserOTP.objects.filter(user=user).update(otp=generate_otp())
        user_otp = UserOTP.objects.get(user=user)
        send_new_otp_email.delay(user.email, user_otp.otp, user.first_name)

        return validated_data


class VerifyEmailSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6, min_length=6)
    email = serializers.EmailField(min_length=2, max_length=100)

    def validate(self, attrs) -> User:
        otp = attrs.get("otp", "")
        email = attrs.get("email", "")
        try:
            user = User.objects.get(email=email)
            UserOTP.objects.get(user=user, otp=otp)
            if not user.is_verified:
                user.is_verified = True
                user.save()
        except User.DoesNotExist or UserOTP.DoesNotExist:
            raise serializers.ValidationError("wrong otp")

        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(min_length=8, write_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, attrs) -> dict[str, str]:
        user = User.objects.get(email=attrs["email"])

        return {
            "refresh": user.tokens()["refresh"],
            "access": user.tokens()["access"],
        }

    class Meta:
        model = User
        fields = ["email", "password", "username", "tokens"]

    def validate(self, attrs) -> dict[str, str]:
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        filtered_user_by_email = User.objects.filter(email=email)

        if (
            filtered_user_by_email.exists()
            and filtered_user_by_email[0].auth_provider != "email"
        ):
            raise AuthenticationFailed(
                detail="Please continue your login using "
                + filtered_user_by_email[0].auth_provider
            )

        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials, try again")
        if not user.is_active:
            raise AuthenticationFailed("Account disabled, contact admin")
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")

        return {
            "email": user.email,
            "tokens": user.tokens,
        }


class CreatePinSerializer(serializers.ModelSerializer):

    """Serializer for pin creation"""

    pin = serializers.CharField(max_length=6, write_only=True)
    pin2 = serializers.CharField(max_length=6, write_only=True)
    email = serializers.EmailField(max_length=255, min_length=3)

    class Meta:
        model = UserPin
        fields = ("email", "pin", "pin2")
        # extra_kwargs = {
        #     "pin": {"required": True},
        #     "last_name": {"write_only": True},
        # }

    def validate(self, attrs) -> User:
        email = attrs.get("email")
        if attrs["pin"] != attrs["pin2"]:
            raise serializers.ValidationError("pins do not match")
        user = UserPin.objects.get(user__email=email)
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")
        # try:
        #     validators.validate_password(password=attrs["password"])
        # except exceptions.ValidationError as e:
        #     raise serializers.ValidationError(str(e))
        return attrs

    @atomic
    def create(self, validated_data) -> UserPin:
        validated_data.pop("pin2")
        UserPin.objects.create(
            user__email=validated_data["email"], pin=hash_pin(validated_data["pin"])
        )

        return validated_data


class PinLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    pin = serializers.CharField(min_length=6, write_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, attrs) -> dict[str, str]:
        user = User.objects.get(email=attrs["email"])

        return {
            "refresh": user.tokens()["refresh"],
            "access": user.tokens()["access"],
        }

    class Meta:
        model = User
        fields = ["email", "pin", "tokens"]

    def validate(self, attrs) -> dict[str, str]:
        email = attrs.get("email", "")
        pin = attrs.get("pin", "")

        filtered_user_by_email = User.objects.filter(email=email)

        if (
            filtered_user_by_email.exists()
            and filtered_user_by_email[0].auth_provider != "email"
        ):
            raise AuthenticationFailed(
                detail="Please continue your login using "
                + filtered_user_by_email[0].auth_provider
            )
        user_pin = UserPin.objects.get(user=filtered_user_by_email)
        pin = verify_pin(pin, user_pin.pin)
        if not pin:
            raise AuthenticationFailed("Invalid credentials, try again")
        if not filtered_user_by_email.is_active:
            raise AuthenticationFailed("Account disabled, contact admin")
        if not filtered_user_by_email.is_verified:
            raise AuthenticationFailed("Email is not verified")

        return {
            "email": filtered_user_by_email.email,
            "tokens": filtered_user_by_email.tokens,
        }


class RequestPasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        model = User
        fields = ["email"]

    def validate(self, attrs) -> User:
        email = attrs.get("email", "")

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            UserOTP.objects.filter(user=user).update(otp=generate_otp())
            user_otp = UserOTP.objects.get(user=user)
            send_password_reset_otp_email.delay(
                user.email, user_otp.otp, user.first_name
            )

        return attrs


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    new_password = serializers.CharField(min_length=6, max_length=68, write_only=True)

    class Meta:
        model = User
        fields = ["old_password", "new_password"]

    def validate(self, attrs) -> User:
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        old_password = attrs.get("old_password", "")
        try:
            user = auth.authenticate(email=user.email, password=old_password)
        except Exception:
            raise serializers.ValidationError({"error": "Wrong password"})
        try:
            validators.validate_password(password=attrs["new_password"])
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})
        RefreshToken(request.user.tokens()["refresh"]).blacklist()

        return attrs

    def create(self, validated_data) -> dict[str, str]:
        request = self.context.get("request")
        user = request.user
        new_password = validated_data["new_password"]
        user.set_password(new_password)
        user.save()

        return user.tokens()


class SetNewPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=68, write_only=True)
    otp = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        model = User
        fields = ["password", "otp"]

    def validate(self, attrs) -> dict[str, str]:
        otp = attrs.get("otp")
        try:
            user = User.objects.get(otp=otp)

            RefreshToken(user.tokens()["refresh"]).blacklist()

            token = user.tokens()
        except User.DoesNotExist:
            raise serializers.ValidationError("The reset otp is invalid", 401)
        try:
            validators.validate_password(password=attrs["password"])
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})

        return token

    def create(self, validated_data) -> str:
        user = User.objects.get(otp=validated_data["otp"])
        user.otp = None
        user.save()
        user.set_password(validated_data["password"])
        password = validated_data["password"]
        user.set_password(password)

        return user.email


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {"bad_token": ("Token is expired or invalid")}

    def validate(self, attrs) -> str:
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs) -> None:
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("bad_token")
