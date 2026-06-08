from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from travelapp.models import Flight, Seat, Booking
from rest_framework.authtoken.models import Token
from travelapp.serializer import UserRegisterSerializer, SeatSerializer, FlightSerializer, BookingSerializer
from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.throttling import ScopedRateThrottle
from travelapp.rate_limiter import rate_limit

class RegisterView(APIView):
    # throttle_classes = [AnonRateThrottle]  # 10 requests/minute per IP
    
    def post(self, request):
        print("Request has hit to this!")
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            print('token has created!')
            return Response({'token':token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    # throttle_classes = [AnonRateThrottle]  # 10 requests/minute per IP
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token':token.key,'userId':user.id})
        return Response({'error':'user does not exist!'},status=status.HTTP_401_UNAUTHORIZED)

@method_decorator(cache_page(60 * 5), name='get')
class List_Create_FlightView(GenericAPIView, mixins.ListModelMixin):
    queryset = Flight.objects.prefetch_related('seats')
    serializer_class = FlightSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

@method_decorator(cache_page(60 * 5), name='get')
class Detail_Update_DestroyView(GenericAPIView, mixins.RetrieveModelMixin):

    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    

class BookingView(APIView):
    permission_classes = [IsAuthenticated]
    # throttle_classes = [ScopedRateThrottle]
    # throttle_scope = 'booking'
    # @rate_limit(max_requests=5, time_window=60)
    def post(self, request):
        seatId = request.data.get('seatId')
        print("We entered the booking view",seatId)
        try:
            seat = Seat.objects.select_for_update().get(id = seatId)

            if seat.is_booked:
                return Response({'error':'Seat is already booked!'}, status = status.HTTP_400_BAD_REQUEST)
            
            seat.is_booked = True
            seat.save()

            booking = Booking.objects.create(
                user = request.user,
                flight = seat.flight,
                business_seat = seat
            )
            
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Seat.DoesNotExist:
            return Response({'error':'seat does not exist'},status=status.HTTP_400_BAD_REQUEST)

class UserBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        if request.user.id != user_id:
            return Response({'error':'Invalid userId!'}, status=status.HTTP_401_UNAUTHORIZED)
        
        bookings = Booking.objects.select_related('user','flight','business_seat').filter(user_id=user_id)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

from django.http import HttpResponse

def health(request):
    return HttpResponse("OK")