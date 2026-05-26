from django.contrib.auth.models import User
from rest_framework import serializers
from travelapp.models import Seat, Flight, Booking

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','email','password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=self.validated_data['username'],
            email = self.validated_data['email'],
            password = self.validated_data['password']
        )
        return user
    
class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id','seat_no', 'flight', 'is_booked', 'features', 'is_business_seat']


class FlightSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, read_only=True)
    class Meta:
        model = Flight
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    flight = serializers.StringRelatedField()
    business_seat = SeatSerializer()
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['user','booking_time','bus','business_seat']