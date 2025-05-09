from django.shortcuts import render, get_object_or_404, redirect

from . import models
from . import forms


def index(request):
    show_modal = request.session.pop('show_promocode_modal', False)
    guest_modal = request.session.pop('show_guest_promocode_modal', False)
    promocode = None

    if request.user.is_authenticated:
        try:
            passenger = models.Passenger.objects.get(user=request.user)
            promocode = passenger.promocode
        except models.Passenger.DoesNotExist:
            pass
    else:
        if guest_modal:
            promocode = request.session.pop('guest_promo', None)

    return render(request, 'flights/index.html', {
        'flights': models.Flight.objects.all(),
        'show_promocode_modal': show_modal or guest_modal,
        'promocode': promocode
    })


    
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
    if request.user.is_authenticated:
        try:
            passenger = models.Passenger.objects.get(user=request.user)
            bookings = models.Booking.objects.filter(passenger=passenger)
        except models.Passenger.DoesNotExist:
            bookings = []
        return render(request, 'flights/booking_detail.html', {'bookings': bookings})

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
