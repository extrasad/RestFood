from ..models import *
from restaurant.models import Restaurant, Dish
from test_helper import TestHelper
from faker import Faker
from random import randint

import json

fake = Faker()

class FoodieProxyTestCase(TestHelper):

    def test_model_create(self):

        [Foodie.objects.create(username=fake.text(randint(x+5, 10)), password=fake.text((x+1)*5),
            email="email_"+str(x)+"@gmail.com") for x in range(0, 4)]

        # Matching

        #Should have 4 User~Foodies 1 created in SetUp and 4 here
        self.assertEqual(len(User.objects.all()), 5)
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
        [Restaurant.objects.create(name=fake.text(randint(x+5, 10)), password=fake.text((x+1)*5),
            email="email_"+str(x)+"@gmail.com", rif=str(x), number_phone=x) for x in range(0, 5)]

        [Restaurant.objects.get(id=x).users_like.add(self.subject.pk) for x in [1, 3, 5]]

        self.assertEqual(len(json.loads(self.subject.get_restaurant_liked)), 3)

    def test_get_dishes_liked(self):
        [Dish.objects.create(restaurant_id=1, name=fake.text(randint(x+5, 10)), description=fake.text((x+1)*5),
            mealtype="pizza") for x in range(0, 5)]

        [Dish.objects.get(id=x).users_like.add(self.subject.pk) for x in [1, 3, 4, 5]]

        self.assertEqual(len(json.loads(self.subject.get_dishes_liked)), 4)

    def test_get_all_following(self):
        tim = Foodie.objects.get_or_create(username='tim')[0]
        chris = Foodie.objects.get_or_create(username='chris')[0]
        carl = Foodie.objects.get_or_create(username='carl')[0]

        [self.subject.relationship.follows.add(x.relationship) for x in [tim, chris, carl]]

        self.assertEqual(len(json.loads(self.subject.get_all_following)), 3)

    def test_get_all_followers(self):
        tim = Foodie.objects.get_or_create(username='tim')[0]
        chris = Foodie.objects.get_or_create(username='chris')[0]
        carl = Foodie.objects.get_or_create(username='carl')[0]

        [x.relationship.follows.add(self.subject.relationship) for x in [tim, chris, carl]]

        self.assertEqual(len(json.loads(self.subject.get_all_followers)), 3)


