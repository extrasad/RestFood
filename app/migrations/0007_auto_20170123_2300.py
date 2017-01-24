# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-23 23:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0006_auto_20170123_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish_review',
            name='users_like',
            field=models.ManyToManyField(blank=True, related_name='dish_review_liked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='restaurant_review',
            name='users_like',
            field=models.ManyToManyField(blank=True, related_name='restaurant_review_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
