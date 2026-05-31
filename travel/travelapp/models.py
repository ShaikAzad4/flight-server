from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Flight(models.Model):
    name = models.CharField(max_length=30)
    start_from = models.CharField(max_length=50)
    reaches_to = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    reach_time = models.DateTimeField()
    buisiness_class_price = models.PositiveIntegerField()
    non_business_class_price = models.PositiveIntegerField()
    no_of_business_class_seets = models.PositiveIntegerField()
    no_of_non_business_class_seets = models.PositiveIntegerField()
    features = models.TextField()
    kilometers = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return f"{self.name} starts from {self.start_from} to {self.reaches_to}"

class Seat(models.Model):
    seat_no = models.CharField(max_length=50)
    flight = models.ForeignKey(Flight,on_delete=models.CASCADE,related_name="seats")
    is_booked = models.BooleanField(default=False)
    features = models.TextField()
    is_business_seat = models.BooleanField(default=False)

    def __str__(self):
        return f"Business CLass Seat No {self.seat_no} for {self.flight.name}"
    


class Booking(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    flight = models.ForeignKey(Flight, models.CASCADE)
    business_seat = models.ForeignKey(Seat, models.CASCADE)