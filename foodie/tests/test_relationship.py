from ..models import *
from test_helper import TestHelper

import json


class RelationshipTestCase(TestHelper):
    def setUp(self):
        self.create_people(['tim', 'chris', 'carl'])

    def test_follow_functionality(self):
        tim = UserExtend.objects.get_or_create(username='tim')[0].foodie
        chris = UserExtend.objects.get_or_create(username='chris')[0].foodie
        carl = UserExtend.objects.get_or_create(username='carl')[0].foodie
        tim.relationship.follows.add(chris.relationship)  # chris follows tim
        tim.relationship.follows.add(carl.relationship)   # carl follows tim
        chris.relationship.follows.add(tim.relationship)

        # Should tim is followed for two users
        self.assertEqual(len(tim.relationship.follows.all()), 2)
        # Should chris following one user
        self.assertEqual(len(chris.relationship.followed_by.all()), 1)
        # Should chris followed for one user
        self.assertEqual(len(chris.relationship.follows.all()), 1)