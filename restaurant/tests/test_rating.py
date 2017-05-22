from ..models import *
from test_helper import TestHelper

import numpy

class RatingTestCase(TestHelper):

    def test_get_rating(self):
        user = self.create_user()
        [Restaurant_Star.objects.create(user_id=user.pk, restaurant_id=self.subject.pk, rating=n)
            for n in self.ratings]
        average_ratings = int(numpy.average(self.ratings))

        # Matching

        # Should numpy average equal to 3
        self.assertEqual(3, average_ratings)
        # Should query and numpy average equal to 3
        self.assertEqual(self.subject.get_rating, average_ratings)