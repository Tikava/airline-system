from django.shortcuts import render, get_object_or_404

from . import models
from . import forms


def index(request):
    flights = models.Flight.objects.all()
    
    context = {
        'flights': flights
    }
    
    return render(request, 'flights/index.html', context)

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
    flight = get_object_or_404(models.Flight, id=flight_id)

    if request.method == 'POST':
        form = forms.PassengerForm(request.POST)

        if form.is_valid():
            booking = form.save() 
            return render(request, 'flights/flight_book_success.html', {'booking': booking})

    else:
        form = forms.PassengerForm(initial={'flight_id': flight.id})

    return render(request, 'flights/flight_book.html', {'form': form, 'flight': flight})


def booking_detail(request):
    
    if request.method == 'POST':
        form = forms.BookingForm(request.POST)
        
        if form.is_valid():
            booking = form.save()
            return render(request, 'flights/booking_detail.html', {'booking': booking})
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
