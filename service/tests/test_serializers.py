from django.test import TestCase
from ..serializers import *
from faker import Faker

fake = Faker()

class SerializeTestCase(TestCase):
    def SetUp(self):
        return


class FoodieInfoSerializerTestCase(SerializeTestCase):

    def test_create(self):
        UserExtend.objects.get_or_create(username='user_1', type="F")
        data = {
                                'foodie': 1,
                                'birthday': str(datetime.date.today()),
                                'gender': 'm' ,
                                'city':'caracas'
                            }
        serializer = FoodieInfoSerializer(data=data)
        serializer.is_valid() # verify if is valid IMPORTANT!
        # serializer.validated_data
        serializer.save()
        self.assertEqual(len(list(Foodie_Info.objects.all())), 1)


class RestaurantInfoSerializerTestCase(SerializeTestCase):

    def test_create(self):
        UserExtend.objects.get_or_create(username='user_1', type="R")
        data = {'restaurant': 1,
                                           'mealtype': 'burger' ,
                                           'slogan': fake.text(10),
                                           'description': fake.text(10)}
        serializer = RestaurantInfoSerializer(data=data)
        serializer.is_valid() # verify if is valid
        # print serializer.validated_data
        serializer.save()
        self.assertEqual(len(list(RestaurantInfo.objects.all())), 1)


class RestaurantSucursalSerializerTestCase(SerializeTestCase):

    def test_create(self):
        UserExtend.objects.get_or_create(username='user_1', type="R")
        json_restaurant_sucursal = {'restaurant': 1,
                                           'city': 'caracas' ,
                                           'address': fake.address(),
                                           'main': True}

        serializer = RestaurantSucursalSerializer(data=json_restaurant_sucursal)
        serializer.is_valid() # verify if is valid
        # print serializer.validated_data
        serializer.save()
        self.assertEqual(len(list(RestaurantSucursal.objects.all())), 1)


class RestaurantReviewSerializerTestCase(SerializeTestCase):

    def test_create(self):
        UserExtend.objects.get_or_create(username='user_1', type="R")
        UserExtend.objects.get_or_create(username="user_1", type="F")
        data = {'restaurant': 1,
                                            'user':1,
                                            'text': fake.text(10)}
        serializer = RestaurantReviewSerializer(data=data)
        serializer.is_valid() # verify if is valid
        serializer.save()
        self.assertEqual(len(list(RestaurantReview.objects.filter(restaurant_id=1).all())), 1)


class DishSerializerTestCase(SerializeTestCase):

    def test_create(self):
        UserExtend.objects.get_or_create(username='user_1', type="R")
        data = {'restaurant': 1,
                                'only_ofert': 'yes',
                                'mealtype': 'burger',
                                'description': fake.text(10),
                                'name':fake.text(8)}
        serializer = DishSerializer(data=data)
        serializer.is_valid() # verify if is valid
        serializer.save()
        self.assertEqual(len(list(Dish.objects.filter(restaurant_id=1).all())), 1)


class DishReviewSerializerTestCase(SerializeTestCase):

    def test_create(self):
        UserExtend.objects.get_or_create(username='user_1', type="R")
        Dish.objects.get_or_create(restaurant_id=1, name=fake.text(10))
        UserExtend.objects.get_or_create(username="user_1", type="F")
        json_dish_review = {'dish': 1,
                            'user':1,
                            'text': fake.text(10)}
        serializer = DishReviewSerializer(data=json_dish_review)
        serializer.is_valid() # verify if is valid
        serializer.save()
        self.assertEqual(len(list(DishReview.objects.filter(dish_id=1).all())), 1)


class OfferSerializerTestCase(SerializeTestCase):

    def test_create(self):
        UserExtend.objects.get_or_create(username='user_1', type="R")
        data = {'name': fake.text(6), 'description' : fake.text(10),
                                 'restaurant': 1}
        serializer = OfferSerializer(data=data)
        serializer.is_valid() # verify if is valid
        serializer.save()
        self.assertEqual(len(list(Offer.objects.filter(restaurant_id=1).all())), 1)