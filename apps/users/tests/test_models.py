from apps.users.tests.base import BaseTest


class TestUserModel(BaseTest):
    """Test the attributes of a user"""

    def test_creating_user_with_necessary_attributes(self):
        """Test user object creation"""

        user = self.user.objects.create_user(**self.user_attr)

        self.assertEqual(user.email, self.user_attr["email"])
        self.assertEqual(user.first_name, self.user_attr["first_name"])
        self.assertEqual(user.last_name, self.user_attr["last_name"])
        self.assertNotEqual(user.password, self.user_attr["password"])
        self.assertIsInstance(user, self.user)

    def test_create_superuser(self):
        """Test user is superuser at creation"""

        user = self.user.objects.create_superuser(**self.user_attr)
        self.assertIsInstance(user, self.user)
        self.assertTrue(user.is_staff, True)
        self.assertTrue(user.is_superuser, True)
        self.assertEqual(user.email, self.user_attr["email"])

    def test_user_email_is_returned_in_dunder_str_method(self):
        """Test user returns email in string method"""

        user = self.user.objects.create_user(**self.user_attr)
        self.assertEqual(user.__str__(), self.user_attr["email"])

    def test_user_tokens_are_returned_on_user_creation(self):
        """Test access and refresh tokens returned on user creation"""

        user = self.user.objects.create_user(**self.user_attr)
        self.assertIn("access", user.tokens())

    def test_email_not_verified_after_user_creation(self):
        """Test user email is not verified at creation"""

        user = self.user.objects.create_user(**self.user_attr)
        self.assertFalse(user.is_verified, False)

    def test_user_is_not_staff_or_superuser(self):
        """Test user is not staff or superuser at creation"""

        user = self.user.objects.create_user(**self.user_attr)
        self.assertFalse(user.is_staff, False)
        self.assertFalse(user.is_superuser, False)

    def test_raises_error_when_user_email_is_not_added(self):
        """Test user creation when email is not provided"""

        self.user_attr["email"] = ""
        with self.assertRaises(ValueError):
            self.user.objects.create_user(**self.user_attr)

    def test_raises_error_when_superuser_is_not_staff(self):
        """Test superuser creation when is_staff is False"""

        is_staff = {"is_staff": False}
        self.user_attr.update(is_staff)
        with self.assertRaises(ValueError):
            self.user.objects.create_superuser(**self.user_attr)

    def test_raises_error_when_superuser_is_not_superuser(self):
        """Test superuser creation when is_superuser is False"""

        is_superuser = {"is_superuser": False}
        self.user_attr.update(is_superuser)
        with self.assertRaises(ValueError):
            self.user.objects.create_superuser(**self.user_attr)
