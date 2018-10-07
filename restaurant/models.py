# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core import serializers
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from core.models import IntegerRangeField
from core.choices import CITY, ONLY_OFERT
from django.db.models import Count
from foodie.models import *

import json, ast


class Restaurant(models.Model):
    user = models.OneToOneField(UserExtend, on_delete=models.CASCADE)
    name = models.CharField(max_length=60, null=True, unique=True)
    rif = models.CharField(max_length=100, null=True, unique=True)
    number_phone = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users_like = models.ManyToManyField(Foodie, through='RestaurantsLikes',
                                        related_name='restaurant_like', blank=True)

    @property
    def total_likes(self):
        return self.users_like.count()

    @property
    def get_rating(self):
        import numpy
        query = Restaurant_Star.objects.values('rating').filter(restaurant_id=self.pk).all()
        return int(numpy.average([x['rating'] for x in query.values()]))

    @property
    def get_total_comment(self):
        return len(RestaurantReview.objects.all())

    def get_last_comment(self, page_index, cant_item, max_item=100):
        from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
        objects = RestaurantReview.objects.filter(restaurant_id=self.pk) \
                      .order_by('-created_at')[:max_item]
        paginator = Paginator(objects, cant_item)
        try:
            comments = paginator.page(page_index)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            comments = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            comments = paginator.page(paginator.num_pages)

        return comments.object_list

    @property
    def get_all_offers(self):
        # https://docs.python.org/2/library/ast.html#ast.literal_eval
        # TODO: Traer fotos de ofertas y platos y los id respectivos
        array_offers = []
        dictionary = {"offers": array_offers}
        for n in Offer.objects.select_related().filter(restaurant_id=self.pk):
            dishes = serializers.serialize('json', list(n.get_all_dish),
                                           fields=('pk', 'name', 'description',
                                           'pizza', 'photo_thumbnail'))
            array_offers.append({
                'name': n.name,
                'description': n.description,
                'dishes': ast.literal_eval(dishes) # Important
            })
        return json.dumps(dictionary).replace('\\"',"\"")

    def most_popular_dishes(self, cant_dishes):
        # TODO: Traer fotos y datos importantes
        array_dishes = []
        query = Dish.objects.filter(restaurant_id=self.pk) \
                   .annotate(like_count_total=Count('users_like')) \
                   .order_by('-like_count_total')[:cant_dishes]    \
                   .values('id', 'name', 'description', 'like_count_total')
        for n in query:
            array_dishes.append(n)
        return json.dumps({'popular_dishes': array_dishes})


class RestaurantsLikes(models.Model):
    class Meta:
        db_table = 'meta_restaurants_likes'
    user = models.ForeignKey(Foodie, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class RestaurantInfo(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)
    mealtype = models.CharField(max_length=15)
    slogan = models.CharField(max_length=112)
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RestaurantSucursal(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    city = models.CharField(max_length=15, choices=CITY, default="caracas")
    address = models.CharField(max_length=112, default="undefined")
    main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RestaurantMediaProfile(models.Model):
    restaurant = models.OneToOneField(Restaurant, on_delete=models.CASCADE)
    banner = models.ImageField(upload_to='restaurant_banner/', default='restaurant_banner/default.jpg')
    banner_thumbnail = ImageSpecField(source='banner',processors=[ResizeToFill(100, 50)],
                                      format='JPEG', options={'quality': 60})
    picture = models.ImageField(upload_to='restaurant_picture/', default='restaurant_picture/default.jpg')
    picture_thumbnail = ImageSpecField(source='picture', processors=[ResizeToFill(100, 50)],
                                       format='JPEG', options={'quality': 60})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Restaurant_Star(models.Model):
    user = models.ForeignKey(Foodie, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rating = IntegerRangeField(min_value=0, max_value=5, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Offer(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=85)
    description = models.CharField(max_length=400)
    photo = models.ImageField(upload_to='food_offers/', default="food_offers/default.jpg")
    photo_thumbnail = ImageSpecField(source='photo', processors=[ResizeToFill(100, 50)],
                                     format='JPEG', options={'quality': 60})

    @property
    def get_all_dish(self):
        return Dish.objects.filter(offer_id=self.pk).all()


class Dish(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, null=True, on_delete=models.CASCADE)
    only_ofert = models.CharField(max_length=3, choices=ONLY_OFERT) #Si el plato es only ofert no se renderizara en la parte de platos del Restaurant
    description = models.CharField(max_length=200)
    name = models.CharField(max_length=85)
    mealtype = models.CharField(max_length=20, default="None")
    prize = models.FloatField(default=0)
    photo = models.ImageField(upload_to='food_dishes/', default="food_dishes/default.jpg")
    photo_thumbnail = ImageSpecField(source='photo',processors=[ResizeToFill(100, 50)],
                                     format='JPEG', options={'quality': 60})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users_like = models.ManyToManyField(Foodie, through='DishesLikes',
                                        related_name='dish_like', blank=True)

    @property
    def total_likes(self):
        return self.users_like.count()


class DishesLikes(models.Model):
    class Meta:
        db_table = 'meta_dishes_likes'
    user = models.ForeignKey(Foodie, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class RestaurantReview(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(Foodie, on_delete=models.CASCADE)
    text = models.CharField(max_length=240)
    users_like = models.ManyToManyField(Foodie, related_name='restaurant_review_like', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_likes(self):
        return self.users_like.count()


class DishReview(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    user = models.ForeignKey(Foodie, on_delete=models.CASCADE)
    text = models.CharField(max_length=120)
    users_like = models.ManyToManyField(Foodie, related_name='dish_review_like', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_likes(self):
        return self.users_like.count()