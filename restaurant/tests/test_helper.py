from django.test import TestCase
from django.contrib.auth.models import User
from ..models import *

class TestHelper(TestCase):

    def setUp(self):
        Restaurant.objects.create(
            name="Restaurant Name",
            password="123456789",
            rif="6666-2144-1244-2426-0080",
            number_phone=0424421442,
            email="restaurant@dominie.com")
        self.subject = Restaurant.objects.get(name="Restaurant Name")
        self.ratings = [2, 5, 3, 3, 5, 1, 5, 2, 5]

    def create_user(self):
        return User.objects.create_user(
            username="javiermaximu",
            password="deadmachine",
            email="javi@gmail.com",
            first_name="Javier",
            last_name="Romero")

    def create_restaurants(self):
        import json, os
        with open(os.path.abspath("restaurant/tests/restaurants.json")) as file:
            restaurant_json = json.load(file)
            for restaurant in restaurant_json['restaurants']:
                this_restaurant = Restaurant.objects.create(
                    name=restaurant['name'],
                    password=restaurant['password'],
                    rif=restaurant['rif'],
                    number_phone=restaurant['number_phone'],
                    email=restaurant['email'])
                try:
                    sucursals = restaurant['sucursal']
                    for sucursal in sucursals:
                        RestaurantSucursal.objects.create(
                            restaurant_id=this_restaurant.pk,
                            city=sucursal['city'],
                            address=sucursal['address'],
                            main=True if sucursal['main'] == 'True' else False)
                except KeyError: pass
                try:
                    information = restaurant['information']
                    RestaurantInfo.objects.create(
                        restaurant_id=this_restaurant.pk,
                        mealtype=information['mealtype'],
                        slogan=information['slogan'],
                        description=information['description'])
                except KeyError: pass
                try:
                    dishes = restaurant['dishes']
                    for dish in dishes:
                        Dish.objects.create(
                            restaurant_id=this_restaurant.pk,
                            name=dish['name'],
                            only_ofert=True if dish['only_ofert'] == 'True' else False,
                            description=dish['description'],
                            prize=dish['prize'],
                            mealtype=dish['mealtype'])
                except KeyError: pass