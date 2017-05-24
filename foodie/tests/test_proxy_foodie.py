from ..models import *
from test_helper import TestHelper
from faker import Faker
from random import randint

fake = Faker()

class FoodieProxyTestCase(TestHelper):

    def test_model_create(self):

        [Foodie.objects.create(username=fake.text(randint(x+5, 10)), password=fake.text(randint(x+5, 10)),
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
