from django.urls import path
from travelapp import views
from travelapp.views import RegisterView, LoginView, BookingView, List_Create_FlightView, UserBookingsView, Detail_Update_DestroyView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('flights/',views.List_Create_FlightView.as_view(), name='buses'),
    path('flight/<int:pk>/',views.Detail_Update_DestroyView.as_view(), name='bus'),
    path('login/',views.LoginView.as_view(), name='login'),
    path('register/',views.RegisterView.as_view(), name='register'),
    path('bookings/',views.BookingView.as_view(), name='booking'),
    path('user/<int:user_id>/bookings/', views.UserBookingsView.as_view(), name='user_bookings'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)