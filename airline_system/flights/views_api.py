from rest_framework import permissions, viewsets

from .models import Flight, Booking
from .serializers import FlightSerializer, BookingSerializer

class FlightViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows flights to be viewed or edited.
    """
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# By booking code
class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bookings to be viewed or edited.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'booking_code'
    lookup_url_kwarg = 'booking_code'
    
    