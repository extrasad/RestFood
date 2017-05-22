from django.test import TestCase
from ..models import *

class RestaurantTestCase(TestCase):

    def create_restaurants(self):
        import json, os
        with open(os.path.abspath("restaurant/tests/restaurants.json")) as file:
            restaurant_json = json.load(file)
            for restaurant in restaurant_json['restaurants']:
                this_restaurant = Restaurant.objects.create(
                    name=restaurant['name'],
                    password=restaurant['password'],
                    rif=restaurant['rif'],
                    number_phone=restaurant['number_phone'],
                    email=restaurant['email'])
                try:
                    sucursals = restaurant['sucursal']
                    for sucursal in sucursals:
                        RestaurantSucursal.objects.create(
                            restaurant_id=this_restaurant.pk,
                            city=sucursal['city'],
                            address=sucursal['address'],
                            main=True if sucursal['main'] == 'True' else False)
                except KeyError: pass
                try:
                    information = restaurant['information']
                    RestaurantInfo.objects.create(
                        restaurant_id=this_restaurant.pk,
                        mealtype=information['mealtype'],
                        slogan=information['slogan'],
                        description=information['description'])
                except KeyError: pass
                try:
                    dishes = restaurant['dishes']
                    for dish in dishes:
                        Dish.objects.create(
                            restaurant_id=this_restaurant.pk,
                            name=dish['name'],
                            only_ofert=True if dish['only_ofert'] == 'True' else False,
                            description=dish['description'],
                            prize=dish['prize'],
                            mealtype=dish['mealtype'])
                except KeyError: pass

    def setUp(self):
        Restaurant.objects.create(
            name="Restaurant Name",
            password="123456789",
            rif="6666-2144-1244-2426-0080",
            number_phone=0424421442,
            email="restaurant@dominie.com")
        self.subject = Restaurant.objects.get(name="Restaurant Name")
    
    def test_create_surcusal(self):
        # Create sucursal relationship
        RestaurantSucursal.objects.create(
            restaurant_id=self.subject.pk,
            city="caracas",
            address="Calle Maria Luisa, Av 76, Sector 24",
            main=True)

        RestaurantSucursal.objects.create(
            restaurant_id=self.subject.pk,
            city="zulia",
            address="Haticos por arriba, calle 56",
            main=False)

        sucursal1 = RestaurantSucursal.objects.filter(city__contains="caracas").first()
        sucursal2 = RestaurantSucursal.objects.filter(city__contains="zulia").first()
        sucursals = RestaurantSucursal.objects.filter(restaurant=self.subject.pk)

        #Matching
        
        # Should sucursal1 id == 1
        self.assertEqual(sucursal1.pk, 1)
        # Should sucursal2 id == 2
        self.assertEqual(sucursal2.pk, 2)
        # Should sucursal1 are the main sucursal
        self.assertTrue(sucursal1.main)
        # Should sucursal1 not are the main sucursal
        self.assertFalse(sucursal2.main)
        # Should subject have two sucursals
        self.assertEqual(len(sucursals), 2)

    def test_create_many_restaurants(self):
        # Create much restaurant info, sucursal and create complex querys
        self.create_restaurants()

        pizza = Restaurant.objects.filter(name__icontains="pizza")
        burguer = Restaurant.objects.filter(name__icontains="burger")
        zulia = RestaurantSucursal.objects.filter(city__icontains="zulia")
        pizza_mealtype = RestaurantInfo.objects.filter(mealtype__icontains="pizza")
        pizza_zulia = RestaurantSucursal.objects.filter(restaurant__name__icontains='pizza',city='zulia')
        coffee_caracas = RestaurantSucursal.objects.filter(restaurant__name__icontains='coffee',
                                                           city='caracas',
                                                           address__icontains='avenida libertador')
        coffe_main_caracas = RestaurantSucursal.objects.filter(restaurant__name__icontains='coffee',
                                                               city='caracas',
                                                               address__icontains='avenida libertador',
                                                               main=True)
        carabobo_pizza_mealtype = Restaurant.objects.filter(name__icontains="pizza",
                                                            restaurantinfo__mealtype__icontains="pizza",
                                                            restaurantsucursal__city__icontains="carabobo")

        #Matching

        # Should have 4 pizza spots searched for the name
        self.assertEqual(len(pizza), 4)
        # Should have 2 hamburguer spots searched for the name
        self.assertEqual(len(burguer), 2)
        # Should have 4 restaurant in Zulia
        self.assertEqual(len(zulia), 7)
        # Should have 2 pizza spots in the city zulia
        self.assertEqual(len(pizza_zulia), 2)
        # Should have 3 coffee spots in caracas av libertador
        self.assertEqual(len(coffee_caracas), 4)
        # Should have 3 coffee spots in caracas av libertador and are the main sucursal
        self.assertEqual(len(coffe_main_caracas), 3)
        # Should have 7 pizza spots searched by the mealtype
        self.assertEqual(len(pizza_mealtype), 7)
        # Should have 1 pizza spot in carabobo searched by the name and mealtype
        self.assertEqual(len(carabobo_pizza_mealtype), 1)

    def test_create_many_dishes(self):
        # Create much dishes and create complex querys
        self.create_restaurants()

        dishes_pizza_by_name = Dish.objects.filter(name__icontains="pizza")
        dishes_pizza_by_mealtype = Dish.objects.filter(mealtype__icontains="pizza")
        burger_by_mealtype = Dish.objects.filter(mealtype__icontains="burger")
        zulia_dish_pizza = Restaurant.objects.filter(restaurantsucursal__city__icontains="zulia",
                                                     dish__mealtype__icontains="pizza").distinct()

        # Matching

        # Should have 3 pizza dish searched by the name
        self.assertEqual(len(dishes_pizza_by_name), 3)
        # Should have 3 pizza dish searched by the mealtype
        self.assertEqual(len(dishes_pizza_by_mealtype), 4)
        # Should have 2 burger dish searched by the mealtype
        self.assertEqual(len(burger_by_mealtype), 2)
        # Should have 1 restaurant in zulia with a dish of pizza
        self.assertEqual(len(zulia_dish_pizza), 1)

    def test_create_category(self):
        # Crear algoritmo que retorne un JSON con todas las categorias que hay
        # de restaurantes, esto no es un attr de alguna tabla, es un elemento
        # que se debera calcular
        pass