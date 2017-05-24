from django.test import TestCase
from ..models import *


class TestHelper(TestCase):

    def setUp(self):
        Foodie.objects.create(
            username="javiermaximu",
            password="deadmachine",
            email="javi@gmail.com",
            first_name="Javier",
            last_name="Romero")