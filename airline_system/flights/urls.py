from django.urls import path
from . import views

app_name = 'flights'
urlpatterns = [
    path('', views.index, name='index'),
    path('airports/<str:code>/', views.airport_detail, name='airport_detail'),
    path('flights/<int:flight_id>/', views.flight_detail, name='flight_detail'),
    path('flights/<int:flight_id>/book/', views.flight_book, name='flight_book'),
    path('bookings/', views.booking_detail, name='booking_detail'),
]