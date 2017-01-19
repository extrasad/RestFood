from __future__ import unicode_literals
from django import forms
from django.db import models
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
    GENDER = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('u', 'Undenifed'),
    )
    """
    attr:   username first_name last_name email password
    method: get_full_name() get_short_name() check_password
    create: create_user(username, email=None, password=None, **extra_fields)
    """
    user = models.ForeignKey(User)
    firstname = models.CharField(max_length=60)
    lastname = models.CharField(max_length=60)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER)
    avatar = models.ImageField(upload_to='user_profile/')

    @property
    def get_age(self):
        import datetime
        return int((datetime.date.today() - self.birthday).days / 365.25)


class Sucursal(Base):
    city = models.CharField(max_length=15) # Change to Choice with all citys in Venezuela
    address = models.CharField(max_length=112)


class Restaurant(Base):
    name = models.CharField(max_length=60)
    password = forms.CharField(widget=forms.PasswordInput)
    rif = models.CharField(max_length=100)
    number_phone = models.IntegerField()
    email = models.EmailField(max_length=45)
    sucursales = models.ManyToManyField(Sucursal, through=u'RestaurantSucursal',
                                        related_name=u'sucursals_restaurant')


class RestaurantSucursal(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    sucursal = models.ForeignKey(Sucursal)
    main = models.BooleanField(default=False)


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
    banner = models.ImageField(upload_to='restaurant_banner/')
    picture = models.ImageField(upload_to='restaurant_picture/')
    

class Restaurant_Info(Base):
    """
    !! cambiar el field de city a choice
    """
    restaurant_id = models.ForeignKey(Restaurant)
    mealtype = models.CharField(max_length=15)
    slogan = models.CharField(max_length=112)
    descripcion = models.CharField(max_length=300)
    city = models.CharField(max_length=15) # Change to Choice with all citys in Venezuela
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
    photo = models.ImageField(upload_to='food_dishes/')