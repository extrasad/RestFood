# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-23 21:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20170114_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant_info',
            name='city',
            field=models.CharField(choices=[('zulia', 'Zulia'), ('caracas', 'Caracas')], max_length=15),
        ),
    ]