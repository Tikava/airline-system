import uuid
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

from rest_framework.response import Response
from rest_framework import status

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'booking_code'
    lookup_url_kwarg = 'booking_code'

    def perform_create(self, serializer):
        serializer.save()         
    


    def create(self, request, *args, **kwargs):
        print("DEBUG - Raw request.data:", request.data)
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            print("❌ VALIDATION FAILED:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        print("✅ VALIDATION PASSED:", serializer.validated_data)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

