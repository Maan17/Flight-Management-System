from django.db.models import Max
from django.test import TestCase, Client

from .models import Airport, Flight, Passenger

# Create your tests here.
class FlightTestCase(TestCase):

    #all thses databases will be created seperately just for testing purposes
    def setUp(self):

        #Create Airports
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        #Create Flights
        Flight.objects.create(origin=a1, destination=a2, duration=100)
        Flight.objects.create(origin=a1, destination=a1, duration=200)
        Flight.objects.create(origin=a1, destination=a2, duration=-100)

    #count the number of departures from the airport
    def test_departures_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(),3)

    #count the number of arrivals from the airport
    def test_arrivals_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(),1)

    #checking whether the flight is valid 
    def test_valid_flight(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=100)
        self.assertTrue(f.is_valid_flight())

    #checking whether the flight is invalid due to destination
    def test_invalid_destination(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())

    #checking whether the flight is invalid due to duration
    def test_invalid_duration(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=-100 )
        self.assertFalse(f.is_valid_flight())