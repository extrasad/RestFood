# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from core.choices import CITY, GENDER


class User_Info(models.Model):
    user = models.ForeignKey(User)
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