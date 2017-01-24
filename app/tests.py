from django.test import TestCase
from models import *


class UserInfoTestCase(TestCase):
    def setUp(self):
        new_user = User_Info.objects.create(
            username="javiermaximu",
            email="javi@gmail.com",
            first_name="Javier",
            last_name="Romero",
            birthday="17/05/1995",
            gender="m",
            avatar=None
        )
