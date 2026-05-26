from django.db.models.signals import post_save
from django.dispatch import receiver
from travelapp.models import Flight, Seat

@receiver(post_save, sender=Flight)
def create_business_class_seats(sender, instance, created, **kwargs):
    if created:
        no_of_seats = instance.no_of_business_class_seets+1
        for i in range(1,no_of_seats):
            Seat.objects.create(
                seat_no = f"{instance.name} B{i}",
                flight = instance,
                features = "Monitor, High speen internet, Food varities, sleepable seats",
                is_business_seat = True
            )

@receiver(post_save, sender=Flight)
def create_non_business_class_seats(sender, instance, created, **kwargs):
    if created:
        no_of_seats = instance.no_of_non_business_class_seets+1
        for i in range(1,no_of_seats+1):
            Seat.objects.create(
                seat_no = f"{instance.name} N-B{i}",
                flight = instance,
                features = ""
            )