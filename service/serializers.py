from rest_framework.serializers import *
from restaurant.models import *


class FoodieInfoSerializer(ModelSerializer):
    avatar = ImageField(required=False)
    birthday = DateField(format='%Y-%m-%d')
    class Meta:
        model = Foodie_Info
        fields = ('id', 'foodie', 'birthday', 'gender', 'city', 'avatar')


class RestaurantInfoSerializer(ModelSerializer):
    class Meta:
        model = RestaurantInfo
        fields = ('id', 'restaurant', 'mealtype', 'slogan', 'description')


class RestaurantSucursalSerializer(ModelSerializer):
    class Meta:
        model = RestaurantSucursal
        fields = ('id', 'restaurant', 'city', 'address', 'main')


class RestaurantReviewSerializer(ModelSerializer):
    class Meta:
        model = RestaurantReview
        fields = ('id', 'restaurant', 'user', 'text')


class DishSerializer(ModelSerializer):
    prize = FloatField(required=False)
    class Meta:
        model = Dish
        fields = ('id', 'restaurant', 'only_ofert',
                  'description', 'name', 'mealtype', 'prize')


class DishReviewSerializer(ModelSerializer):
    class Meta:
        model = DishReview
        fields = ('id', 'dish', 'user', 'text')

class OfferSerializer(ModelSerializer):
    photo = ImageField(required=False)
    class Meta:
        model = Offer
        fields = ('name', 'description', 'restaurant', 'photo')