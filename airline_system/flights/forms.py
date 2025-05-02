from django import forms
from django.core.exceptions import ValidationError


from .models import Passenger, Booking, Flight

class PassengerForm(forms.Form):
    flight_id = forms.IntegerField(widget=forms.HiddenInput())

    def save(self, user):
        flight_id = self.cleaned_data['flight_id']
        flight = Flight.objects.get(id=flight_id)

        if flight.capacity <= 0:
            raise ValidationError("No available seats for this flight.")

        passenger, created = Passenger.objects.get_or_create(user=user, defaults={'name': user.username})

        if Booking.objects.filter(passenger=passenger, flight=flight).exists():
            raise ValidationError("You have already booked this flight.")

        booking = Booking.objects.create(passenger=passenger, flight=flight)
        flight.capacity -= 1
        flight.save()

        return booking



    

class BookingForm(forms.Form):
    booking_code = forms.UUIDField(
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    def clean_booking_code(self):
        booking_code = self.cleaned_data.get('booking_code')
        if not Booking.objects.filter(booking_code=booking_code).exists():
            raise forms.ValidationError("Booking code does not exist.")
        return booking_code

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not Booking.objects.filter(passenger__user__email=email).exists():
            raise forms.ValidationError("Email does not match any booking.")
        return email

    def save(self):
        booking_code = self.cleaned_data['booking_code']
        email = self.cleaned_data['email']
        return Booking.objects.get(
            booking_code=booking_code, 
            passenger__user__email=email
        )
