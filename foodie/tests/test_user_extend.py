from ..models import *
from restaurant.models import Restaurant, Dish, RestaurantReview, DishReview
from test_helper import TestHelper
from faker import Faker
from random import randint

import json, datetime, pytz

fake = Faker()

class UserExtendTestCase(TestHelper):

    def test_model_create(self):
        for x in range(0, 4):

           user = UserExtend.objects.create(type="F", username=str(x) + fake.text(randint(x+5, 8)),
                                            password=str(x)+fake.text((x+1)*5), email=str(x) + fake.email())

        # Matching

        #Should have 4 User~Foodies 1 created in SetUp and 4 here
        self.assertEqual(len(UserExtend.objects.all()), 5)
        # Should have 4 User~Foodies 1 created in SetUp and 4 here
        self.assertEqual(len(Foodie.objects.all()), 5)
        # Should have property for return restaurant liked
        self.assertTrue(hasattr(Foodie, 'get_restaurant_liked'))
        # Should have property for return dishes liked
        self.assertTrue(hasattr(Foodie, 'get_dishes_liked'))
        # Should have a customer property that following
        self.assertTrue(hasattr(Foodie, 'get_all_following'))
        # Should have a customer property that are follower
        self.assertTrue(hasattr(Foodie, 'get_all_followers'))
        # Should have a property that returns the most recent activity
        self.assertTrue(hasattr(Foodie, 'get_recent_activity'))

    def test_get_restaurant_liked(self):
        for x in range(0, 5):
            user = UserExtend.objects.create(type="R", password=fake.text((x+5)), email="email_"+str(x)+"@gmail.com")
            Restaurant.objects.filter(pk=user.pk).update(rif= str(x), number_phone=0424421442)

        [Restaurant.objects.get(id=x).users_like.add(self.subject.pk) for x in [1, 3, 5]]

        self.assertEqual(len(json.loads(self.subject.get_restaurant_liked)), 3)

    def test_get_dishes_liked(self):
        [Dish.objects.create(restaurant_id=1, name=fake.text(randint(x+5, 10)), description=fake.text((x+1)*5),
                             mealtype="pizza") for x in range(0, 5)]

        [Dish.objects.get(id=x).users_like.add(self.subject.pk) for x in [1, 3, 4, 5]]

        self.assertEqual(len(json.loads(self.subject.get_dishes_liked)), 4)

    def test_get_all_following(self):
        peoples = self.create_people(['tim', 'chris', 'carl'])

        [self.subject.relationship.follows.add(x.relationship) for x in peoples]

        self.assertEqual(len(json.loads(self.subject.get_all_following)), 3)

    def test_get_all_followers(self):
        peoples = self.create_people(['tim', 'chris', 'carl'])

        [x.relationship.follows.add(self.subject.relationship) for x in peoples]

        self.assertEqual(len(json.loads(self.subject.get_all_followers)), 3)


    def test_get_recent_activity(self):
        user_1, user_2, user_3, user_4, user_5 = self.create_people(['user_1', 'user_2', 'user_3', 'user_4', 'user_5'])

        #  user_1 follow user_2, user_3, user_4 but not to user_5, fuck off user_5

        [self.subject.relationship.follows.add(x.relationship) for x in [user_1, user_2, user_3, user_4]]
        user_restaurant = UserExtend.objects.create(type="R", password="123456789", email="restaurant@dominie.com")
        restaurant_for_like = Restaurant.objects.filter(user_id=user_restaurant.pk).first()
        dish_for_like_1 = Dish.objects.create(restaurant_id=1, name="Burger",
                                    description=fake.text(10), mealtype="pizza")
        dish_for_like_2 = Dish.objects.create(restaurant_id=1, name="Burger",
                                    description=fake.text(10), mealtype="pizza")

        #  user_1 -> follow -> user_5
        user_1.relationship.follows.add(user_5.relationship)
        #  user_2 -> like -> dish
        dish_for_like_1.users_like.add(user_2.pk)
        #  user_3 -> review -> restaurant
        RestaurantReview.objects.create(restaurant_id=1, user_id=user_3.pk, text=fake.text(10))
        #  user_3 -> like -> restaurant
        restaurant_for_like.users_like.add(user_3.pk)
        #  user_3 -> follow -> user_4
        user_3.relationship.follows.add(user_4.relationship)
        #  user_3 -> like -> dish
        dish_for_like_2.users_like.add(user_3.pk)
        #  user_2 -> follow -> user_4
        user_2.relationship.follows.add(user_4.relationship)
        # user_4 -> review -> dish
        DishReview.objects.create(dish_id=1, user_id=user_4.pk, text=fake.text(10))
        # user_5 -> review > restaurant | Este deberia ser ignorado porque no lo sigue self.subject
        RestaurantReview.objects.create(restaurant_id=1, user_id=user_5.pk, text=fake.text(10))

        # TODO: la funcion debe agarrar 6 resultados y ver si pueden ser variantes, no todos de la misma tabla
        self.assertEqual(len(json.loads(self.subject.get_recent_activity(6))), 6)
