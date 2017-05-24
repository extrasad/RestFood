# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from core.choices import CITY, GENDER


class Foodie(User):
    class Meta:
        proxy = True

    @property
    def get_restaurant_liked(self):
        return
    
    @property
    def get_dishes_liked(self):
        return

    @property
    def get_all_following(self):
        return

    @property
    def get_all_followers(self):
        return
    
    @property
    def get_recent_activity(self):
        return 


class Foodie_Info(models.Model):
    user = models.ForeignKey(Foodie)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER)
    city = models.CharField(max_length=15, choices=CITY, default="caracas")
    avatar = models.ImageField(upload_to='user_profile/', default='user_profile/default.jpg')
    avatar_thumbnail = ImageSpecField(source='avatar', processors=[ResizeToFill(100, 50)],
                                      format='JPEG', options={'quality': 60})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_age(self):
        import datetime
        return int((datetime.date.today() - self.birthday).days / 365.25)