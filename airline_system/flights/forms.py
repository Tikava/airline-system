from django import forms

from .models import Passenger, Booking, Flight

class PassengerForm(forms.Form):
    name = forms.CharField(
        max_length=100, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    flight_id = forms.IntegerField(widget=forms.HiddenInput())

    def clean_email(self):
        email = self.cleaned_data.get('email')
        flight_id = self.data.get('flight_id') or self.cleaned_data.get('flight_id')

        if not flight_id:
            raise forms.ValidationError("Flight ID is missing.")

        if Booking.objects.filter(passenger__email=email, flight_id=flight_id).exists():
            raise forms.ValidationError("This email is already registered for this flight.")

        return email

    def save(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        flight_id = self.cleaned_data['flight_id']

        flight = Flight.objects.get(id=flight_id)
        
        if flight.capacity > 0:
            flight.capacity -= 1
            flight.save()
        else:
            raise forms.ValidationError("No available seats for this flight.")

        passenger, _ = Passenger.objects.get_or_create(email=email, defaults={'name': name})
        booking = Booking.objects.create(passenger=passenger, flight=flight)

        return booking


    

class BookingForm(forms.Form):
    booking_code = forms.UUIDField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    def clean_booking_code(self):
        booking_code = self.cleaned_data.get('booking_code')
        if not Booking.objects.filter(booking_code=booking_code).exists():
            raise forms.ValidationError("Booking code does not exist.")
        return booking_code
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not Booking.objects.filter(passenger__email=email).exists():
            raise forms.ValidationError("Email does not match any booking.")
        return email
    
    def save(self):
        booking_code = self.cleaned_data['booking_code']
        email = self.cleaned_data['email']
        booking = Booking.objects.get(booking_code=booking_code, passenger__email=email)
        return booking