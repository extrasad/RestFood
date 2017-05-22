from django.test import TestCase
from django.contrib.auth.models import User

class TestHelper(TestCase):
    def test_return_user(self):
        return User.objects.create_user(
            username="javiermaximu",
            password="deadmachine",
            email="javi@gmail.com",
            first_name="Javier",
            last_name="Romero")