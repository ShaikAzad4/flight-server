from django.contrib import admin
from travelapp.models import Flight, Seat, Booking
# Register your models here.
@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('name','start_from','reaches_to','non_business_class_price')
@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('seat_no','flight','is_booked','features','is_business_seat')