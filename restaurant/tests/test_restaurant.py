from django.test import TestCase
from ..models import *

class RestaurantTestCase(TestCase):
    
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

    def test_many_restaurants_sucursal(self):
        # Create much restaurant and sucursal and create complex querys
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
                except KeyError:
                    pass

        pizza = Restaurant.objects.filter(name__icontains="pizza")
        burguer = Restaurant.objects.filter(name__icontains="burger")
        zulia = RestaurantSucursal.objects.filter(city__icontains="zulia")
        pizza_zulia = RestaurantSucursal.objects.filter(restaurant__name__icontains='pizza', city='zulia')
        coffee_caracas = RestaurantSucursal.objects.filter(
                                                    restaurant__name__icontains='coffee',
                                                    city='caracas',
                                                    address__icontains='avenida libertador')
        coffe_main_caracas = RestaurantSucursal.objects.filter(
                                                    restaurant__name__icontains='coffee',
                                                    city='caracas',
                                                    address__icontains='avenida libertador',
                                                    main=True)

        #Matching

        # print [x.address for x in coffee_caracas if x.address]
        
        # Should have 4 pizza spots searched for the name
        self.assertEqual(len(pizza), 4)
        # Should have 2 hamburguer spots searched for the name
        self.assertEqual(len(burguer), 2)
        # Should have 4 restaurant in Zulia
        self.assertEqual(len(zulia), 7)
        # Should have 2 pizza spots in the city zulia
        self.assertEqual(len(pizza_zulia), 2)
        # Should have 3 coffee sports in caracas av libertador
        self.assertEqual(len(coffee_caracas), 4)
        # Should have 3 coffee sports in caracas av libertador and are the main sucursal
        self.assertEqual(len(coffe_main_caracas), 3)
    
    def test_many_restaurants_information(self):
        # Create much restaurant and information and create complex querys
        pass