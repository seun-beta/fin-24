from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient


class BaseTest(TestCase):
    """Base class for tests"""

    user = get_user_model()
    client = APIClient()
    user_attr = user_attr = {
        "email": "easteregg@gmail.com",
        "phone_number": "+23412345678",
        "first_name": "Easter",
        "last_name": "Egg",
        "password": "12w2qsz2`123x@Aw2:",
    }

    def setUp(self):
        """Run before every test case"""

        self.user_attr = {
            "email": "easteregg@gmail.com",
            "phone_number": "+23412345678",
            "first_name": "Easter",
            "last_name": "Egg",
            "password": "12w2qsz2`123x@Aw2:",
        }

    def tearDown(self):
        """Run after every test case"""

        self.user.objects.all().delete()
