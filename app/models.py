from __future__ import unicode_literals
from django import forms
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.contrib.auth.models import User

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class Base(models.Model):
    id = models.AutoField(primary_key=True)
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
    GENDER = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('u', 'Undenifed'),
    )
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


class Sucursal(Base):
    city = models.CharField(max_length=15) # Change to Choice with all citys in Venezuela
    address = models.CharField(max_length=112)
    main = models.BooleanField(default=False)


class Restaurant(Base):
    name = models.CharField(max_length=60)
    password = forms.CharField(widget=forms.PasswordInput)
    rif = models.CharField(max_length=100)
    number_phone = models.IntegerField()
    email = models.EmailField(max_length=45)
    sucursales = models.ManyToManyField(Sucursal, through=u'RestaurantSucursal', related_name=u'sucursals_restaurant')


class RestaurantSucursal(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    sucursal = models.ForeignKey(Sucursal)

class User_Star(Base):
    user = models.ForeignKey(User_Info)
    calification = IntegerRangeField(min_value=0, max_value=5, default=0)
    stars = models.ManyToManyField(Restaurant)


class Restaurant_Media(Base):
    """
    !! crear imagenes default y
    sus carpetas
    """
    restaurant_id = models.ForeignKey(Restaurant)
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


class Restaurant_Info(Base):
    """
    !! cambiar el field de city a choice
    """

    CITY = (
        ('zulia', 'Zulia'), ('caracas', 'Caracas'), ('valencia', 'Valencia'),
        ('barquisimeto', 'Barquisimeto'), ('maracay','Maracay'), (' ciudad guayana', ' Ciudad Guayana'),
        ('san cristobal', 'San Cristobal'), ('barcelona', 'Barcelona'), ('maturin', 'Maturin'),
        ('ciudad bolivar', 'Ciudad Bolivar'), ('puerto la cruz', 'Puerto La Cruz'), ('merida', 'Merida'),
        ('punto fijo', 'Punto Fijo'), ('los teques', 'Los Teques'), ('acarigua', 'Acarigua'),
        ('carabobo', 'Carabobo'), ('valera', 'Valera'), ('apure', 'Apure'), ('coro', 'Coro'),
        ('puerto cabello', 'Puerto Cabello')
    )
    restaurant_id = models.ForeignKey(Restaurant)
    mealtype = models.CharField(max_length=15)
    slogan = models.CharField(max_length=112)
    descripcion = models.CharField(max_length=300)
    city =  models.CharField(max_length=15, choices=CITY)
    address = models.CharField(max_length=112)


class Food_Dishes(Base):
    """
    >Si el plato es only ofert no se
    renderizara en la parte de platos
    del Restaurant
    >Si prize es 0 entonces se ocultara
    el precio
    """
    ONLY_OFERT = (
        ('yes', 'Yes only ofert'),
        ('no', 'No only ofert'),
    )
    restaurant_id = models.ForeignKey(Restaurant)
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

class Restaurant_Review(Base):
    restaurant_id = models.ForeignKey(Restaurant)
    user_id = models.ForeignKey(User_Info)
    text = models.CharField(max_length=240)
    users_like = models.ManyToManyField(
        User,
        related_name='restaurant_review_liked',
        blank=True
    )

    @property
    def total_likes(self):
        return self.users_like.count()

class Dish_Review(Base):
    dish_id = models.ForeignKey(Food_Dishes)
    user_id = models.ForeignKey(User_Info)
    text = models.CharField(max_length=120)
    users_like = models.ManyToManyField(
        User,
        related_name='dish_review_liked',
        blank=True
    )
    @property
    def total_likes(self):
        return self.users_like.count()
