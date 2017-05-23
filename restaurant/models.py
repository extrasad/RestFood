# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.core import serializers
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from core.models import IntegerRangeField
from core.choices import CITY, ONLY_OFERT
from foodie.models import User


class Restaurant(models.Model):
    name = models.CharField(max_length=60, null=False, unique=True)
    password = models.CharField(max_length=25, null=False, unique=True)
    rif = models.CharField(max_length=100, null=False, unique=True)
    number_phone = models.IntegerField()
    email = models.EmailField(max_length=45, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users_like = models.ManyToManyField(User, related_name='restaurant_like', blank=True)

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
        import json
        dictionary = {}
        for n in Offer.objects.select_related().filter(restaurant_id=self.pk):
            dishes = serializers.serialize('json', list(n.get_all_dish),
                                           fields=('pk', 'name', 'description',
                                                   'pizza', 'photo_thumbnail'))
            # dictionary["offer"][n.name] = json.dumps({'name':n.name, 'description': n.description})
            # meter titulo y descripcion, pk de la oferta en dishes serializado y listo
            print dishes
        # print dictionary


class RestaurantInfo(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    mealtype = models.CharField(max_length=15)
    slogan = models.CharField(max_length=112)
    description = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RestaurantSucursal(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    city = models.CharField(max_length=15, choices=CITY, default="caracas")
    address = models.CharField(max_length=112, default="undefined")
    main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class RestaurantMedia(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    banner = models.ImageField(upload_to='restaurant_banner/', default='restaurant_banner/default.jpg')
    banner_thumbnail = ImageSpecField(source='banner',processors=[ResizeToFill(100, 50)],
                                      format='JPEG', options={'quality': 60})
    picture = models.ImageField(upload_to='restaurant_picture/', default='restaurant_picture/default.jpg')
    picture_thumbnail = ImageSpecField(source='picture', processors=[ResizeToFill(100, 50)],
                                       format='JPEG', options={'quality': 60})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Restaurant_Star(models.Model):
    user = models.ForeignKey(User)
    restaurant = models.ForeignKey(Restaurant)
    rating = IntegerRangeField(min_value=0, max_value=5, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Offer(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    name = models.CharField(max_length=85)
    description = models.CharField(max_length=400)
    photo = models.ImageField(upload_to='food_offers/', default="food_offers/default.jpg")
    photo_thumbnail = ImageSpecField(source='photo', processors=[ResizeToFill(100, 50)],
                                     format='JPEG', options={'quality': 60})

    @property
    def get_all_dish(self):
        return Dish.objects.filter(offer_id=self.pk).all()


class Dish(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    offer = models.ForeignKey(Offer, null=True)
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
    users_like = models.ManyToManyField(User, related_name='dish_like', blank=True)
    @property
    def total_likes(self):
        return self.users_like.count()


class RestaurantReview(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    user = models.ForeignKey(User)
    text = models.CharField(max_length=240)
    users_like = models.ManyToManyField(User, related_name='restaurant_review_like', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_likes(self):
        return self.users_like.count()


class DishReview(models.Model):
    dish = models.ForeignKey(Dish)
    user = models.ForeignKey(User)
    text = models.CharField(max_length=120)
    users_like = models.ManyToManyField(User, related_name='dish_review_like', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_likes(self):
        return self.users_like.count()