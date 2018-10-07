from ..models import *
from restaurant.tests.test_helper import TestHelper

class RestaurantTestCase(TestHelper):

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