from ..models import *
from test_helper import TestHelper

import numpy

class RatingTestCase(TestHelper):

    # def setUp(self):
    #     Restaurant.objects.create(
    #         name="Restaurant Name",
    #         password="123456789",
    #         rif="6666-2144-1244-2426-0080",
    #         number_phone=0424421442,
    #         email="restaurant@dominie.com")
    #
    #     self.subject = Restaurant.objects.get(name="Restaurant Name")
    #     self.ratings = [2, 5, 3, 3, 5, 1, 5, 2, 5]

    def test_get_rating(self):
        user = self.test_return_user()
        [Restaurant_Star.objects.create(user_id=user.pk, restaurant_id=self.subject.pk, rating=n) for n in self.ratings]
        average_ratings = int(numpy.average(self.ratings))

        # Matching

        # Should numpy average equal to 3
        self.assertEqual(3, average_ratings)
        # Should query and numpy average equal to 3
        self.assertEqual(self.subject.get_rating, average_ratings)