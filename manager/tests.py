import datetime

from django.test import TestCase
from cities.models import Country, City, Region
from django.core.exceptions import ValidationError

from manager.models import Sede, Building


class SedeTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name="testCountry",
                                              slug="test",
                                              code="TE",
                                              code3="TES",
                                              population=1000,
                                              area=1000,
                                              currency="$",
                                              currency_name="ARS",
                                              languages="es",
                                              phone="250",
                                              continent="AF",
                                              tld="rw",
                                              capital="asd")

        self.state = Region.objects.create(name_std="test",
                                           code="test",
                                           country=self.country)

        self.city = City.objects.create(name_std="test",
                                        location='POINT(-120.18444970926208 50.65664762026928)',
                                        population=1000,
                                        region=self.state,
                                        country=self.country,
                                        elevation=1000,
                                        kind="ADM1",
                                        timezone="America/Argentina/Buenos_Aires")

        self.building = Building.objects.create(name="test", slug="test", address="test 123")

    def test_url_validation(self):
        """
        Tests that the url validation regex for sede is correct
        """
        sede = Sede.objects.create(country=self.country, state=self.state, city=self.city, name="test",
                                   date=datetime.date.today(), place=self.building, url="This_IS_Correct")

        self.assertIsNotNone(sede, "Sede created correctly")

    def test_url_validation_not_ok(self):
        """
        Tests that the url validation regex for sede raises exception when incorrect
        """
        self.assertRaises(ValidationError, Sede.objects.create, country=self.country, state=self.state, city=self.city,
                          name="test", date=datetime.date.today(), place=self.building, url="This&IS?NOT/OK")
