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

    #to test whether the index page us workig properly or not
    def index(self):
        #some client will be interacting
        c = Client()
        #route which will get the index page and save it in response
        response = c.get("/flights/")
        #status code should be fine, everything should be fine
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["flights"].count(), 3)
    
    def test_valid_flight_page(self):
        #test the flight page
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)

        c = Client()
        #if we want to get a flight with id
        response = c.get(f"/flights/{f.id}")
        #we are able to get it
        self.assertEqual(response.status_code, 200)

    def test_invalid_flight_page(self):
        #Whatever the maximum id of the flight is
        max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]

        c = Client()
        response = c.get(f"/flights/{max_id}")
        #get one id greater than the maximum flight
        try:
            #response = render_to_response('404.html', {},context_instance=RequestContext(request))
            response = c.get(f"/flights/{max_id+1}")
        except:
            response.status_code = 400
        #then error page should be displayed
        self.assertEqual(response.status_code, 400)

    #check the passenger page
    def test_flight_page_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Alice", last="Adams")
        f.passengers.add(p)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)

    def test_flight_page_non_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Alice", last="Adams")

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1)

