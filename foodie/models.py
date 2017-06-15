# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core import serializers
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from core.choices import CITY, GENDER
from core.models import AutoOneToOneField, UserExtend
from django.utils import timezone
from itertools import chain

import datetime
import restaurant.models


class Foodie(models.Model):
    user = models.OneToOneField(UserExtend)

    @property
    def get_restaurant_liked(self):
        return serializers.serialize(
            'json', list(restaurant.models.Restaurant.objects.filter(
                users_like__id=self.pk)
            )
        )

    @property
    def get_dishes_liked(self):
        return serializers.serialize(
            'json', list(restaurant.models.Dish.objects.filter(
                users_like__id=self.pk)
            )
        )

    @property
    def get_all_followers(self):
        return serializers.serialize(
            'json', list(self.relationship.followed_by.all())
        )

    @property
    def get_all_following(self):
        return serializers.serialize(
            'json', list(self.relationship.follows.all())
        )


    def get_recent_activity(self, limit, days=30):
        """
        :param limit: Cantidad maxima de QuerySet por cada consulta 
        :param days:  Intervalos de dias en los cuales buscar actividad
        :return: Un objecto complejo con la combinacion de las consultas hechas.
        
        :algorithm:
            1.) Calculo la fecha de hoy menos limit en el formato correcto para la consulta
            2.) Verifico si self sigue a alguien, si no es asi retorno False
            3.) Consulto en DishReview, ResturantReview
            4.) Junto todos los QuerySet y lo serializo en formato json
        """
        # TODO solo agarra los review -> todo -> Consultar likes y relationships
        # TODO Cuando este metodo este listo para su uso, solo se usara cada 12 horasy el resultado se debera
        # TODO guardar en las cookies.
        days = timezone.now() - datetime.timedelta(days=days) # Calculo la fecha de hoy con los dias maximos para buscar
        # Primero intento conseguir los id de los usuarios seguidos por self
        id_follows =  [x['user_id'] for x in list(self.relationship.follows.values('user_id').all())]
        if len(id_follows) == 0:
            return False # Significa que self no sigue a nadie

        # Review Dish creada por las personas que sigues
        recent_dish_review = restaurant.models.DishReview. \
                                       objects.filter(user_id__in=id_follows,
                                                      created_at__lte=timezone.now(),
                                                      created_at__gte=days
                                                      ).order_by('-created_at')[:limit]

        # Review Restaurant creada por las personas que sigues
        recent_restaurant_review = restaurant.models.RestaurantReview. \
                                       objects.filter(user_id__in=id_follows,
                                                      created_at__lte=timezone.now(),
                                                      created_at__gte=days
                                                      ).order_by('-created_at')[:limit]

        # Usuarios que sigues y like un Dish
        recent_like_dish = restaurant.models.DishesLikes. \
                                       objects.filter(user_id__in=id_follows,
                                                      created_at__lte=timezone.now(),
                                                      created_at__gte=days
                                                      ).order_by('-created_at')[:limit]

        # TODO cuando termine de hacer todas la consultas debo tranformar los datos y normalizarlos

        return serializers.serialize(
            'json', list(sorted(chain(recent_restaurant_review, recent_dish_review, recent_like_dish)))
        )


class RelationShip(models.Model):
    user = AutoOneToOneField(Foodie)
    follows = models.ManyToManyField('RelationShip', related_name='followed_by')

    def __unicode__(self):
        return self.user.username


class Foodie_Info(models.Model):
    foodie = models.OneToOneField(Foodie)
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