from django.db import models

# Create your models here.

class Airport(models.Model):
    code=models.CharField(max_length=3)
    city=models.CharField(max_length=64)
    def __str__(self):
        return f"{self.city} ({self.code})"

class Flight(models.Model):
    #origin is now a foreign key referencing another table flight
    #models.CASCADE means if we want to delete an airport from the
    #airports table it's going to also delete any of the corresponding flights
    #related name gives all the departured=s from the airport which in return give all of the leaving flights
    origin=models.ForeignKey(Airport,on_delete=models.CASCADE,related_name="departures")
    destination=models.ForeignKey(Airport,on_delete=models.CASCADE,related_name="arrivals")
    duration=models.IntegerField()

    #returning string representation
    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"

class Passenger(models.Model):       
    first=models.CharField(max_length=64)
    last=models.CharField(max_length=64)
    #passengers have many to many relationship with flights
    #a flight could have multiple passengers and a passenger could be on multiple flights
    flights=models.ManyToManyField(Flight,blank=True, related_name="passengers")

    def __str__(self):
        return f"{self.first} {self.last}"