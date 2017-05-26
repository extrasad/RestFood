from django.test import TestCase
from restaurant.models import *
from ..serializers import *
from faker import Faker
from django.utils.six import BytesIO
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

fake = Faker()

class SerializeTestCase(TestCase):
    def SetUp(self):
        return

class FoodieSerializerTestCase(SerializeTestCase):

    def test_read(self):
        foodie = Foodie(username=fake.text(10), password=fake.password(),
                        first_name=fake.first_name(), last_name=fake.last_name(),
                        email=fake.email())
        foodie.save()
        serializer = FoodieSerializer(foodie)

        self.assertEqual(len(serializer.data), 6)

    def test_create(self):
        json_foodie = json.dumps({ 'username': fake.text(10),
                                'password':fake.password(),
                                'first_name':fake.first_name(),
                                'last_name':fake.last_name(),
                                'email':fake.email() })

        stream = BytesIO(json_foodie)
        data = JSONParser().parse(stream)

        serializer = FoodieSerializer(data=data)
        serializer.is_valid() # verify if is valid
        serializer.validated_data
        serializer.save()
        self.assertEqual(len(list(Foodie.objects.all())), 1)

    def test_many_query_set(self):
        # Si le paso many=True puedo serializer directamente los QuerySet
        user_1 = Foodie.objects.get_or_create(username='user_1')[0]
        user_2 = Foodie.objects.get_or_create(username='user_2')[0]
        user_3 = Foodie.objects.get_or_create(username='user_3')[0]
        user_4 = Foodie.objects.get_or_create(username='user_4')[0]
        user_5 = Foodie.objects.get_or_create(username='user_5')[0]
        serializer = FoodieSerializer(Foodie.objects.all(), many=True)
        self.assertEqual(len(serializer.data), 5)

class FoodieInfoSerializerTestCase(SerializeTestCase):

    def test_create(self):
        json_foodie_info = json.dumps({'user_id': 1,
                                'birthday': str(datetime.date.today()),
                                'gender': 'm' ,
                                'city':'caracas'})

        stream = BytesIO(json_foodie_info)
        data = JSONParser().parse(stream)

        serializer = Foodie_InfoSerializer(data=data)
        print serializer.is_valid() # verify if is valid
        print serializer.validated_data
        serializer.save()
        self.assertEqual(len(list(Foodie_Info.objects.all())), 1)

class RestaurantSerializerTestCase(SerializeTestCase):
    def test_create(self):
        pass


class RestaurantInfoSerializerTestCase(SerializeTestCase):

    def test_create(self):
        pass

class RestaurantReviewSerializerTestCase(SerializeTestCase):

    def test_create(self):
        pass

class DishSerializerTestCase(SerializeTestCase):

    def test_create(self):
        pass

class DishRevireSerializerTestCase(SerializeTestCase):

    def test_create(self):
        pass