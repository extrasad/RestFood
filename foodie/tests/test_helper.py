from django.test import TestCase
from django.shortcuts import get_object_or_404
from ..models import *


class TestHelper(TestCase):

    def setUp(self):
        user = UserExtend.objects.create(type="F", username="javiermaximu",
                                         password="deadmachine", email="javi@gmail.com",
                                         first_name="Javier", last_name="Romero")
        self.subject = get_object_or_404(Foodie, user_id=user.pk)

    def create_people(self, list_people):
        [UserExtend.objects.create(username=x, type="F") for x in list_people]
        peoples = Foodie.objects.filter(user__username__in=list_people).all()
        return list(peoples)

