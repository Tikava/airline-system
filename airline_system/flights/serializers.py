from rest_framework import serializers

from .models import Flight, Booking


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ['id', 'origin', 'destination', 'duration', 'capacity']
        read_only_fields = ['id']
        

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'passenger', 'flight', 'booking_code']
        read_only_fields = ['id', 'booking_code']
        extra_kwargs = {
            'passenger': {'required': True},
            'flight': {'required': True}
        }
        depth = 1
        
        
        