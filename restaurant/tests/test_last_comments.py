from ..models import *
from test_helper import TestHelper
from faker import Faker
from random import randint

fake = Faker()

class CreateCommentTestCase(TestHelper):

    def test_total_comment(self):
        user = self.create_user()
        [RestaurantReview.objects.create(restaurant_id=self.subject.pk, user_id=user.pk,
            text=fake.text(randint(10, 35)))for x in range(0, 25)]

        # Matching

        # Should have 25 comment
        self.assertEqual(self.subject.get_total_comment, 25)

    def test_last_comment(self):
        user = self.create_user()
        [RestaurantReview.objects.create(restaurant_id=self.subject.pk, user_id=user.pk,
            text=fake.text(randint(10, 35))) for x in range(0, 5)]

        last_comments = self.subject.get_last_comment(1, 5)

        # Matching

        # Should first date is greater than the second date
        self.assertGreater(last_comments[0].created_at, last_comments[1].created_at)