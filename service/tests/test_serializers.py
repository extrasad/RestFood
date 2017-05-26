from django.test import TestCase
from ..serializers import *
from faker import Faker
from django.utils.six import BytesIO
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
        Foodie.objects.get_or_create(username='user_1')
        json_foodie_info = json.dumps({
                                'user': 1,
                                'birthday': str(datetime.date.today()),
                                'gender': 'm' ,
                                'city':'caracas'
                            })
        stream = BytesIO(json_foodie_info)
        data = JSONParser().parse(stream)

        serializer = FoodieInfoSerializer(data=data)
        serializer.is_valid() # verify if is valid IMPORTANT!
        # serializer.validated_data
        serializer.save()
        self.assertEqual(len(list(Foodie_Info.objects.all())), 1)


class RestaurantSerializerTestCase(SerializeTestCase):

    def test_create(self):
        json_restaurant_info = json.dumps({'name': fake.name(),
                                           'password': fake.password(),
                                           'rif': '124124141',
                                           'number_phone': '12312',
                                           'email': fake.email()})

        stream = BytesIO(json_restaurant_info)
        data = JSONParser().parse(stream)
        serializer = RestaurantSerializer(data=data)
        serializer.is_valid() # verify if is valid
        # print serializer.validated_data
        serializer.save()
        self.assertEqual(len(list(Restaurant.objects.all())), 1)


class RestaurantInfoSerializerTestCase(SerializeTestCase):

    def test_create(self):
        Restaurant.objects.get_or_create(name=fake.text(10))
        json_restaurant_info = json.dumps({'restaurant': 1,
                                           'mealtype': 'burger' ,
                                           'slogan': fake.text(10),
                                           'description': fake.text(10)})

        stream = BytesIO(json_restaurant_info)
        data = JSONParser().parse(stream)
        serializer = RestaurantInfoSerializer(data=data)
        serializer.is_valid() # verify if is valid
        # print serializer.validated_data
        serializer.save()
        self.assertEqual(len(list(RestaurantInfo.objects.all())), 1)


class RestaurantSucursalSerializerTestCase(SerializeTestCase):

    def test_create(self):
        Restaurant.objects.get_or_create(name=fake.text(10))
        json_restaurant_sucursal = json.dumps({'restaurant': 1,
                                           'city': 'caracas' ,
                                           'address': fake.address(),
                                           'main': True})

        stream = BytesIO(json_restaurant_sucursal)
        data = JSONParser().parse(stream)
        serializer = RestaurantSucursalSerializer(data=data)
        serializer.is_valid() # verify if is valid
        # print serializer.validated_data
        serializer.save()
        self.assertEqual(len(list(RestaurantSucursal.objects.all())), 1)


class RestaurantReviewSerializerTestCase(SerializeTestCase):

    def test_create(self):
        Restaurant.objects.get_or_create(name=fake.text(10))
        Foodie.objects.get_or_create(username="user_1")
        json_restaurant_review = json.dumps({'restaurant': 1,
                                            'user':1,
                                            'text': fake.text(10)})

        stream = BytesIO(json_restaurant_review)
        data = JSONParser().parse(stream)
        serializer = RestaurantReviewSerializer(data=data)
        serializer.is_valid() # verify if is valid
        serializer.save()
        self.assertEqual(len(list(RestaurantReview.objects.filter(restaurant_id=1).all())), 1)


class DishSerializerTestCase(SerializeTestCase):

    def test_create(self):
        Restaurant.objects.get_or_create(name=fake.text(10))
        json_dish = json.dumps({'restaurant': 1,
                                'only_ofert': 'yes',
                                'mealtype': 'burger',
                                'description': fake.text(10),
                                'name':fake.text(8)})

        stream = BytesIO(json_dish)
        data = JSONParser().parse(stream)
        serializer = DishSerializer(data=data)
        serializer.is_valid() # verify if is valid
        serializer.save()
        self.assertEqual(len(list(Dish.objects.filter(restaurant_id=1).all())), 1)


class DishReviewSerializerTestCase(SerializeTestCase):

    def test_create(self):
        Restaurant.objects.get_or_create(name=fake.text(10))
        Dish.objects.get_or_create(restaurant_id=1, name=fake.text(10))
        Foodie.objects.get_or_create(username="user_1")
        json_dish_review = json.dumps({'dish': 1,
                                       'user':1,
                                       'text': fake.text(10)})

        stream = BytesIO(json_dish_review)
        data = JSONParser().parse(stream)
        serializer = DishReviewSerializer(data=data)
        serializer.is_valid() # verify if is valid
        serializer.save()
        self.assertEqual(len(list(DishReview.objects.filter(dish_id=1).all())), 1)

class OfferSerializerTestCase(SerializeTestCase):

    def test_create(self):
        Restaurant.objects.get_or_create(name=fake.text(10))
        json_offer = json.dumps({'name': fake.text(6), 'description' : fake.text(10),
                                 'restaurant': 1})

        stream = BytesIO(json_offer)
        data = JSONParser().parse(stream)
        serializer = OfferSerializer(data=data)
        serializer.is_valid() # verify if is valid
        serializer.save()
        self.assertEqual(len(list(Offer.objects.filter(restaurant_id=1).all())), 1)