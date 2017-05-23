from ..models import *
from test_helper import TestHelper
from faker import Faker

import json

fake = Faker()

class CreateOfferTestCase(TestHelper):

    def test_create_offers(self):
        self.create_offers()
        all_offer = json.loads(self.subject.get_all_offers)

        # Matching

        # Should the name of offer equal to Big Craze Burguers!
        self.assertEqual(all_offer['offers'][0]['name'], 'Big Craze Burguers!')
        # Should the name of offer equal to PizzaIce Monster!
        self.assertEqual(all_offer['offers'][1]['name'], 'PizzaIce Monster!')
