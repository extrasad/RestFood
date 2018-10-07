from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from ..models import *

import json, os


class TestHelper(TestCase):

    def setUp(self):
        user = UserExtend.objects.create(type="R", password="123456789", email="restaurant@dominie.com")
        Restaurant.objects.filter(pk=user.pk).update(
            name="Restaurant Name",
            rif="6666-2144-1244-2426-0080",
            number_phone="0424421442")
        self.subject = Restaurant.objects.get(name="Restaurant Name")
        self.ratings = [2, 5, 3, 3, 5, 1, 5, 2, 5]

    def create_user(self):
        user = UserExtend.objects.create(type="F", username="javiermaximu",
                                         password="deadmachine", email="javi@gmail.com",
                                         first_name="Javier", last_name="Romero")
        return get_object_or_404(Foodie, user_id=user.pk)

    def create_restaurants(self):
        with open(os.path.abspath("restaurant/tests/restaurants.json")) as file:
            restaurant_json = json.load(file)
            for restaurant in restaurant_json['restaurants']:
                user_restaurant = UserExtend.objects.create(type="R", password=restaurant['password'], email=restaurant['email'])
                Restaurant.objects.filter(pk=user_restaurant.pk).update(
                    name=restaurant['name'],
                    rif=restaurant['rif'],
                    number_phone=restaurant['number_phone'])
                this_restaurant = get_object_or_404(Restaurant, user_id=user_restaurant.pk)
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

    def create_offers(self):
        with open(os.path.abspath("restaurant/tests/offers.json")) as file:
            offer_json = json.load(file)
            for offer in offer_json['offers']:
                this_offer = Offer.objects.create(
                    restaurant_id=self.subject.pk,
                    name=offer['name'],
                    description=offer['description'])
                for dish in offer['dishes']:
                    Dish.objects.create(
                        restaurant_id=self.subject.pk,
                        offer_id=this_offer.pk,
                        name=dish['name'],
                        description=dish['description'],
                        mealtype=dish['mealtype'])

    def create_dish_and_likes(self):
        with open(os.path.abspath("restaurant/tests/dishes.json")) as file:
            dishes_json = json.load(file)
            for dish in dishes_json['dishes']:
                this_dish = Dish.objects.create(
                    restaurant_id=self.subject.pk,
                    name=dish['name'],
                    description=dish['description'])
                for user in dish['likes']:
                    DishesLikes.objects.create(user_id=user['user_id'], dish_id=this_dish.pk)