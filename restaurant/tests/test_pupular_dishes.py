from ..models import *
from test_helper import TestHelper

import json

class PopularDishesTestCase(TestHelper):

    def test_get_popular_dishes(self):
        self.create_dish_and_likes()

        popular_dishes = json.loads(self.subject.most_popular_dishes(3))

        # Matching

        # Should the name of offer most popular equal to Super Rico Mexican
        self.assertEqual(popular_dishes['popular_dishes'][0]['name'], 'Super Rico Mexican')
        # Should dish Super Rico Mexican have 5 likes
        self.assertEqual(popular_dishes['popular_dishes'][0]['like_count_total'], 5)
        # Should the name of offer medium popular equal to ChocoSadly
        self.assertEqual(popular_dishes['popular_dishes'][1]['name'], 'ChocoSadly')
        # Should dish ChocoSadly have 4 likes
        self.assertEqual(popular_dishes['popular_dishes'][1]['like_count_total'], 4)
        # Should the name of offer low popular equal to Sphagetti Loco
        self.assertEqual(popular_dishes['popular_dishes'][2]['name'], 'Sphagetti Loco')
        # Should dish Sphagetti Loco have 3 likes
        self.assertEqual(popular_dishes['popular_dishes'][2]['like_count_total'], 3)