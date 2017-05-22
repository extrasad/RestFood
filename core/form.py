from django import forms
from choices import *

class SearchRestaurant(forms.Form):
    city = forms.CharField()
    meal = forms.CharField()

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

class UserRegistration(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField()
    last_name = forms.CharField()
    birthday = forms.DateField()
    gender = forms.ChoiceField(GENDER)
    avatar = forms.ImageField()

class RestaurantRegistration(forms.Form):
    name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    rif = forms.CharField()
    number_phone = forms.IntegerField()
    email = forms.EmailField()


