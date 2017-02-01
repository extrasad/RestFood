from django.test import TestCase
from django.contrib.auth.models import User
from models import *

class CreateUser(TestCase):
    def test_return_user(self):
        return User.objects.create_user(
            username="javiermaximu",
            password="deadmachine",
            email="javi@gmail.com",
            first_name="Javier",
            last_name="Romero",
        )

class UserInfoTestCase(CreateUser):
    def setUp(self):
        User.objects.create_user(
            username="lion",
            email="jose@gmail.com",
            password="kakaroto")
        User.objects.create_user(
            username="cat",
            email="javifu@gmail.com",
            password="merenge")

    def test_user_creation(self):
        w = self.test_return_user()
        self.assertTrue(isinstance(w, User))
        self.assertEqual(w.__unicode__(), w.username)

    def test_user_pk(self):
        lion = User.objects.get(username="lion")
        # lion.pk is guaranteed to always be 1
        w = self.test_return_user()
        self.assertEqual(lion.pk, 1)
        self.assertEqual(w.pk, 3)

    def test_create_info_user(self):
        lion = User.objects.get(username="lion")
        User_Info.objects.create(
            user_id=lion.pk,
            birthday=u"2005-2-04",
            gender='Male')
        lion_info = User_Info.objects.get(user_id=lion.pk)
        self.assertEqual(lion_info.pk, 1)
        self.assertEqual(lion_info.get_age, 11)

class RestaurantTestCase(CreateUser):
    def setUp(self):
        Restaurant.objects.create(
            name="Pizza Sad Life",
            password="muerte241241",
            rif="1244-2144-1244-2426-0080",
            number_phone=0424421442,
            email="sadliferest@gmail.com"
        )

    def test_create_sucursal(self):
        rest = Restaurant.objects.get(name="Pizza Sad Life")

        RestaurantSucursal.objects.create(
            restaurant_id=rest.pk,
            city="caracas",
            address="Calle Maria Luisa, Av 76, Sector 24",
            main=True
        )

        RestaurantSucursal.objects.create(
            restaurant_id=rest.pk,
            city="zulia",
            address="Haticos por arriba, calle 56",
            main=False
        )

        sucursal1 = RestaurantSucursal.objects.filter(city__contains="caracas").first()
        sucursal2 = RestaurantSucursal.objects.filter(city__contains="zulia").first()

        self.assertEqual(sucursal1.pk, 1)
        self.assertEqual(sucursal2.pk, 2)
        self.assertTrue(sucursal1.main)
        self.assertFalse(sucursal2.main)

        sucursals = RestaurantSucursal.objects.\
            filter(restaurant=rest.pk)

        count_sucursals = len(sucursals)

        self.assertEqual(count_sucursals, 2)

    def test_user_star_restaurant(self):
        w = self.test_return_user()
        rest = Restaurant.objects.get(name="Pizza Sad Life")
        numbers = [2, 5, 3]
        for n in numbers:
            User_Star.objects.create(
                user_id=w.pk,
                restaurant_id=rest.pk,
                calification=n
            )

        stars = User_Star.objects.values('calification')\
            .filter(user_id=w.pk,
                   restaurant_id=rest.pk)\
                    .all()

        stars_len = len(stars)
        self.assertEqual(stars_len, 3)
        stars_sum = 0
        for n in stars.values():
            stars_sum += n['calification']

        stars_prom = stars_sum/len(stars)
        self.assertEqual(stars_sum, 10)
        self.assertEqual(stars_prom, 3)

        # (2 + 5 + 3) / 3 = 3
