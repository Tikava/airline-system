from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from . import views_api

router = DefaultRouter()
router.register(r'flights', views_api.FlightViewSet, basename='flight')
router.register(r'bookings', views_api.BookingViewSet, basename='booking')


app_name = 'flights'
urlpatterns = [
    path('', views.index, name='index'),
    path('airports/<str:code>/', views.airport_detail, name='airport_detail'),
    path('flights/<int:flight_id>/', views.flight_detail, name='flight_detail'),
    path('flights/<int:flight_id>/book/', views.flight_book, name='flight_book'),
    path('bookings/', views.booking_detail, name='booking_detail'),
    path('api/', include(router.urls)),
]