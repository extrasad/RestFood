from rest_framework.serializers import *
from restaurant.models import *


# class Meta: MAS CORTO PERO MENOS DETALLADO
#     model = Snippet
#     fields = ('id', 'title', 'code', 'linenos', 'language', 'style')

# TODO: hacer los serializer de los demas modelos
class FoodieSerializer(Serializer):
    id = IntegerField(read_only=True)
    first_name  =  CharField(required=False, max_length=100)
    last_name   =  CharField(required=False, max_length=100)
    email       =  EmailField()
    username    =  CharField()
    password    =  CharField()

    def create(self, validated_data):
        return Foodie.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance


class Foodie_InfoSerializer(Serializer):
    id       =  IntegerField(read_only=True)
    user_id  =  IntegerField()
    birthday =  DateField(format='%Y-%m-%d')
    gender   =  ChoiceField(choices=GENDER)
    city     =  ChoiceField(choices=CITY, default="caracas")
    avatar   =  ImageField(required=False)

    def create(self, validated_data):
        return Foodie_Info.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.city = validated_data.get('city', instance.city)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()
        return instance