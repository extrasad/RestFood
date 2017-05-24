from ..models import *
from test_helper import TestHelper

import json


class RelationshipTestCase(TestHelper):

    def test_follow_functionality(self):
        tim = Foodie.objects.get_or_create(username='tim')[0]
        chris = Foodie.objects.get_or_create(username='chris')[0]
        carl = Foodie.objects.get_or_create(username='carl')[0]
        tim.relationship.follows.add(chris.relationship)  # chris follows tim
        tim.relationship.follows.add(carl.relationship)   # carl follows tim
        chris.relationship.follows.add(tim.relationship)

        # Should tim is followed for two users
        self.assertEqual(len(tim.relationship.follows.all()), 2)
        # Should chris following one user
        self.assertEqual(len(chris.relationship.followed_by.all()), 1)
        # Should chris followed for one user
        self.assertEqual(len(chris.relationship.follows.all()), 1)