from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


from .models import Passenger, Booking, Flight

class PassengerForm(forms.Form):
    flight_id = forms.IntegerField(widget=forms.HiddenInput())

    def save(self, user):
        flight_id = self.cleaned_data['flight_id']
        flight = Flight.objects.get(id=flight_id)

        if flight.capacity <= 0:
            raise ValidationError("No available seats for this flight.")

        # Get or create passenger linked to the current user
        passenger, created = Passenger.objects.get_or_create(user=user, defaults={'name': user.username})

        # Avoid double booking
        if Booking.objects.filter(passenger=passenger, flight=flight).exists():
            raise ValidationError("You have already booked this flight.")

        # Create booking and reduce flight capacity
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

    

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError("Passwords do not match.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    

from django.contrib.auth import authenticate

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password.")
        return cleaned_data
