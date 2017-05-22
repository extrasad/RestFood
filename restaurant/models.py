# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import User
from choices import *


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Restaurant(Base):
    name = models.CharField(max_length=60, null=False, unique=True)
    password = models.CharField(max_length=25, null=False, unique=True)
    rif = models.CharField(max_length=100, null=False, unique=True)
    number_phone = models.IntegerField()
    email = models.EmailField(max_length=45, null=False, unique=True)


class Restaurant_Info(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    mealtype = models.CharField(max_length=15)
    slogan = models.CharField(max_length=112)
    descripcion = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RestaurantSucursal(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    city = models.CharField(max_length=15, choices=CITY, default="caracas") # Change to Choice with all citys in Venezuela
    address = models.CharField(max_length=112, default="undefined")
    main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Restaurant_Media(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    banner = models.ImageField(upload_to='restaurant_banner/', default='restaurant_banner/default.jpg')
    banner_thumbnail = ImageSpecField(source='banner',processors=[ResizeToFill(100, 50)],
                                      format='JPEG', options={'quality': 60})
    picture = models.ImageField(upload_to='restaurant_picture/', default='restaurant_picture/default.jpg')
    picture_thumbnail = ImageSpecField(source='picture', processors=[ResizeToFill(100, 50)],
                                       format='JPEG', options={'quality': 60})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Restaurant_Review(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    user = models.ForeignKey(User)
    text = models.CharField(max_length=240)
    users_like = models.ManyToManyField(User, related_name='restaurant_review_liked', blank=True)

    @property
    def total_likes(self):
        return self.users_like.count()

class Dish(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    only_ofert = models.CharField(max_length=3, choices=ONLY_OFERT) #Si el plato es only ofert no se renderizara en la parte de platos del Restaurant
    description = models.CharField(max_length=400)
    name = models.CharField(max_length=45)
    mealtype = models.CharField(max_length=20, default="None")
    prize = models.FloatField(default=0)
    photo = models.ImageField(upload_to='food_dishes/', default="food_dishes/default.jpg")
    photo_thumbnail = ImageSpecField(source='photo',processors=[ResizeToFill(100, 50)],
                                     format='JPEG', options={'quality': 60})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Dish_Review(models.Model):
    dish = models.ForeignKey(Dish)
    user = models.ForeignKey(User)
    text = models.CharField(max_length=120)
    users_like = models.ManyToManyField(User, related_name='dish_review_liked', blank=True)
    
    @property
    def total_likes(self):
        return self.users_like.count()