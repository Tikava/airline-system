import uuid
from django.contrib.auth.models import User
from django.db import models

class Airport(models.Model):
    code = models.CharField(max_length=3, unique=True)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.city}"

class Flight(models.Model):
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.origin} to {self.destination} ({self.duration} min)"


class Passenger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.user.email})"

class Booking(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    booking_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def __str__(self):
        return f"Booking {self.booking_code} - {self.passenger} for {self.flight}"
