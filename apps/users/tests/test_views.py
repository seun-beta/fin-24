from unittest import mock

from django.urls import reverse

from rest_framework import status

from apps.users.tests.base import BaseTest


class TestRegisterUserAPIView(BaseTest):
    """Test RegisterUserAPIView"""

    def test_register_user_with_valid_data(self):
        """Test registering user with valid data"""

        extra_data = {"password2": "12w2qsz2`123x@Aw2:"}
        self.user_attr.update(extra_data)
        response = self.client.post(reverse("register"), self.user_attr)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["email"], self.user_attr["email"])
        self.assertEqual(response.data["phone_number"], self.user_attr["phone_number"])
        self.assertEqual(response.data["first_name"], self.user_attr["first_name"])
        self.assertEqual(response.data["last_name"], self.user_attr["last_name"])
        self.assertIsNone(response.data.get("password"), None)
        self.assertIsNone(response.data.get("password2"), None)

    def test_register_user_with_passwords_that_do_not_match(self):
        """Test registering users with passwords that do not match"""

        extra_data = {"password2": "12w2qz2`123x@Aw2:"}
        self.user_attr.update(extra_data)
        response = self.client.post(reverse("register"), self.user_attr)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_with_invalid_password(self):
        """Test registering users with invalid password"""

        extra_data = {"password2": "1ez212322123"}
        self.user_attr["password"] = "1ez212322123"
        self.user_attr.update(extra_data)
        response = self.client.post(reverse("register"), self.user_attr)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestRequestNewOTPAPIView(BaseTest):
    """Test  RequestNewOTPAPIView"""

    def test_request_new_otp_with_already_verified_email(self):
        """Test requesting new otp with already verified email"""

        user = self.user.objects.create_user(**self.user_attr)
        user.is_verified = True
        user.save()

        response = self.client.post(
            reverse("new_otp"), {"email": "easteregg@gmail.com"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], ["email is already verified"])

    def test_request_new_otp(self):
        """Test requesting new otp"""

        self.user.objects.create_user(**self.user_attr)

        response = self.client.post(
            reverse("new_otp"), {"email": self.user_attr["email"]}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestVerifyEmailAPIView(BaseTest):
    """Test  VerifyEmailAPIView"""

    @mock.patch("apps.utility.mail_service.send_new_otp_email")
    def test_verify_email_with_correct_otp(self, new_otp_mock):
        """Test email verification with correct OTP"""

        new_otp_mock.return_value = None
        user = self.user.objects.create_user(**self.user_attr)
        user.otp = "123456"
        user.save()

        response = self.client.post(reverse("email_verify"), {"otp": "123456"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_email_with_wrong_otp(self):
        """Test email verification with wrong OTP"""

        response = self.client.post(reverse("email_verify"), {"otp": "113456"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestLoginAPIView(BaseTest):
    """Test  LoginAPIView"""

    def test_login_with_correct_credentials(self):
        """Test login with correct credentials"""

        user = self.user.objects.create_user(**self.user_attr)
        user.is_verified = True
        user.save()

        response = self.client.post(
            reverse("login"),
            {
                "email": self.user_attr["email"],
                "password": self.user_attr["password"],
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data["tokens"])
        self.assertIsNotNone(response.data["tokens"]["access"])
        self.assertIsNotNone(response.data["tokens"]["refresh"])
        # self.assertEqual(response.data["tokens"]["access"], user.tokens()["access"])
        # self.assertEqual(response.data["tokens"]["refresh"], user.tokens()["refresh"])

    def test_login_with_incorrect_credentials(self):
        """Test login with incorrect credentials"""

        self.user.objects.create_user(**self.user_attr)

        response = self.client.post(
            reverse("login"),
            {"email": "ade@gmail.com", "password": self.user_attr["password"]},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_with_disabled_account(self):
        """Test login with with disabled account credentials"""

        user = self.user.objects.create_user(**self.user_attr)
        user.is_active = False
        user.save()

        response = self.client.post(
            reverse("login"),
            {
                "email": self.user_attr["email"],
                "password": self.user_attr["password"],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "Account disabled, contact admin")
