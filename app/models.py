from __future__ import unicode_literals
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import User
from choices import *

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class User_Info(Base):
    """
    attr:   username first_name last_name email password
    method: get_full_name() get_short_name() check_password
    create: create_user(username, email=None, password=None, **extra_fields)
    print profile.avatar_thumbnail.url     /media/CACHE/images/982d5af84cddddfd0fbf70892b4431e4.jpg
    print profile.avatar_thumbnail.width  100
    """
    user = models.ForeignKey(User)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER)
    avatar = models.ImageField(upload_to='user_profile/', default='user_profile/default.jpg')
    avatar_thumbnail = ImageSpecField(source='avatar',
                                      processors=[ResizeToFill(100, 50)],
                                      format='JPEG',
                                      options={'quality': 60})
    @property
    def get_age(self):
        import datetime
        return int((datetime.date.today() - self.birthday).days / 365.25)


class Restaurant(Base):
    name = models.CharField(max_length=60, null=False, unique=True)
    password = models.CharField(max_length=25, null=False, unique=True)
    rif = models.CharField(max_length=100, null=False, unique=True)
    number_phone = models.IntegerField()
    email = models.EmailField(max_length=45, null=False, unique=True)


class RestaurantSucursal(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    city = models.CharField(max_length=15, choices=CITY, default="caracas") # Change to Choice with all citys in Venezuela
    address = models.CharField(max_length=112, default="undefined")
    main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class User_Star(models.Model):
    user = models.ForeignKey(User_Info)
    restaurant = models.ForeignKey(Restaurant)
    calification = IntegerRangeField(min_value=0, max_value=5, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Restaurant_Media(models.Model):
    """
    !! crear imagenes default y
    sus carpetas
    """
    restaurant = models.ForeignKey(Restaurant)
    banner = models.ImageField(upload_to='restaurant_banner/', default='restaurant_banner/default.jpg')

    banner_thumbnail = ImageSpecField(source='banner',
                                      processors=[ResizeToFill(100, 50)],
                                      format='JPEG',
                                      options={'quality': 60})

    picture = models.ImageField(upload_to='restaurant_picture/', default='restaurant_picture/default.jpg')

    picture_thumbnail = ImageSpecField(source='picture',
                                      processors=[ResizeToFill(100, 50)],
                                      format='JPEG',
                                      options={'quality': 60})

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Restaurant_Info(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    mealtype = models.CharField(max_length=15)
    slogan = models.CharField(max_length=112)
    descripcion = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Food_Dishes(models.Model):
    """
    >Si el plato es only ofert no se
    renderizara en la parte de platos
    del Restaurant
    >Si prize es 0 entonces se ocultara
    el precio
    """
    restaurant = models.ForeignKey(Restaurant)
    only_ofert = models.CharField(max_length=3, choices=ONLY_OFERT)
    description = models.CharField(max_length=400)
    name = models.CharField(max_length=45)
    mealtype = models.CharField(max_length=20, default="None")
    prize = models.FloatField(default=0)
    photo = models.ImageField(upload_to='food_dishes/', default="food_dishes/default.jpg")

    photo_thumbnail = ImageSpecField(source='photo',
                                      processors=[ResizeToFill(100, 50)],
                                      format='JPEG',
                                      options={'quality': 60})

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Restaurant_Review(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    user = models.ForeignKey(User_Info)
    text = models.CharField(max_length=240)
    users_like = models.ManyToManyField(
        User,
        related_name='restaurant_review_liked',
        blank=True
    )

    @property
    def total_likes(self):
        return self.users_like.count()

class Dish_Review(models.Model):
    dish = models.ForeignKey(Food_Dishes)
    user = models.ForeignKey(User_Info)
    text = models.CharField(max_length=120)
    users_like = models.ManyToManyField(
        User,
        related_name='dish_review_liked',
        blank=True
    )
    @property
    def total_likes(self):
        return self.users_like.count()
