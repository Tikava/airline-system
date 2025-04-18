from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout

from . import models
from . import forms


def index(request):
    flights = models.Flight.objects.all()
    
    context = {
        'flights': flights
    }
    
    return render(request, 'flights/index.html', context)

def logout_view(request):
    logout(request)
    return render(request, 'flights/logout.html')

def register_view(request):
    if request.method == 'POST':
        form = forms.UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            models.Passenger.objects.create(user=user, name=user.username)
            login(request, user)
            return redirect('flights:index')

        else:
            return render(request, 'flights/register.html', {'form': form})
    else:
        form = forms.UserRegistrationForm()
    
    return render(request, 'flights/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = forms.UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('flights:index')
            else:
                return render(request, 'flights/login.html', {
                    'form': form,
                    'error': 'Invalid username or password.'
                })
    else:
        form = forms.UserLoginForm()
    
    return render(request, 'flights/login.html', {'form': form})

        
    
def flight_detail(request, flight_id):
    flight = models.Flight.objects.get(id=flight_id)
    bookings = models.Booking.objects.filter(flight=flight)
    passengers = [booking.passenger for booking in bookings]
    
    context = {
        'flight': flight,
        'passengers': passengers,
    }
    return render(request, 'flights/flight_detail.html', context)

def flight_book(request, flight_id):
    
    if request.user.is_authenticated:
        flight = get_object_or_404(models.Flight, id=flight_id)

        passenger, _ = models.Passenger.objects.get_or_create(
            user=request.user,
            defaults={'name': request.user.username}
        )


        existing_booking = models.Booking.objects.filter(passenger=passenger, flight=flight).first()
        if existing_booking:
            return render(request, 'flights/flight_booked_already.html', {
                'booking': existing_booking,
                'flight': flight
            })


        if request.method == 'POST':
            form = forms.PassengerForm(request.POST)
            if form.is_valid():
                try:
                    booking = form.save(request.user)
                    return render(request, 'flights/flight_book_success.html', {'booking': booking})
                except forms.ValidationError as e:
                    form.add_error(None, e.message)
        else:
            form = forms.PassengerForm(initial={'flight_id': flight.id})

        return render(request, 'flights/flight_book.html', {'form': form, 'flight': flight})

    else:
        return redirect('flights:login')


def booking_detail(request):
    # If user is logged in — show all their bookings
    if request.user.is_authenticated:
        try:
            passenger = models.Passenger.objects.get(user=request.user)
            bookings = models.Booking.objects.filter(passenger=passenger)
        except models.Passenger.DoesNotExist:
            bookings = []
        return render(request, 'flights/booking_detail.html', {'bookings': bookings})

    # If not logged in — allow guest to search by form
    if request.method == 'POST':
        form = forms.BookingForm(request.POST)
        if form.is_valid():
            try:
                booking = form.save()
                return render(request, 'flights/booking_single.html', {'booking': booking})
            except models.Booking.DoesNotExist:
                form.add_error(None, "Booking not found.")
    else:
        form = forms.BookingForm()

    return render(request, 'flights/booking_form.html', {'form': form})



def airport_detail(request, code):
    airport = models.Airport.objects.get(code=code)
    departures = airport.departures.all()
    arrivals = airport.arrivals.all()
    context = {
        'airport': airport,
        'departures': departures,
        'arrivals': arrivals
    }
    return render(request, 'flights/airport_detail.html', context)
