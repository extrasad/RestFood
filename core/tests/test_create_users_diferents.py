from django.test import TestCase
from restaurant.models import Foodie, UserExtend, Restaurant

class CreateUserRestaurant(TestCase):
    def setUp(self):
        return

    def test_create_user_foodie(self):
        user = UserExtend.objects.create(username="fafafa",
                                         password="21313sadfas",
                                         first_name="John",
                                         last_name="Smith",
                                         email="ohn.smith@xyz.com",
                                         type="F")
        self.assertEqual(user.id, 1)
        self.assertEqual(UserExtend.objects.filter(id=user.id).first().type, 'F')
        self.assertEqual(len(Foodie.objects.filter(user_id=user.id)), 1)

    def test_create_user_restaurant(self):
        user = UserExtend.objects.create(password="21313sadfas",
                                         email="ohn.smith@xyz.com",
                                         type="R")
        self.assertEqual(user.id, 1)
        self.assertEqual(UserExtend.objects.filter(id=user.id).first().type, 'R')
        self.assertEqual(UserExtend.objects.filter(id=user.id).first().username, 'ohn.smith@xyz.com_1')
        self.assertEqual(len(Restaurant.objects.filter(user_id=user.id)), 1)