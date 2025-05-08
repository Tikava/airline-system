from flights.models import Passenger


class FirstVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                passenger = Passenger.objects.get(user=request.user)
                if not passenger.promocode:
                    promocode = self.generate_random_promocode()
                    passenger.promocode = promocode
                    passenger.save()
                    request.session['show_promocode_modal'] = True
            except Passenger.DoesNotExist:
                pass
        return self.get_response(request)

    def generate_random_promocode(self):
        import random, string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
