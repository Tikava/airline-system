from flights.models import Passenger
import random
import string

class FirstVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            if not request.COOKIES.get('first_visit_done'):
                promo = self.generate_random_promocode()
                request.session['guest_promo'] = promo
                request.session['show_guest_promocode_modal'] = True
        else:
            try:
                passenger = Passenger.objects.get(user=request.user)
                if not passenger.promocode:
                    promocode = self.generate_random_promocode()
                    passenger.promocode = promocode
                    passenger.save()
                    request.session['show_promocode_modal'] = True
            except Passenger.DoesNotExist:
                pass

        response = self.get_response(request)

        if not request.user.is_authenticated and not request.COOKIES.get('first_visit_done'):
            response.set_cookie('first_visit_done', 'yes', max_age=60*60*24*365)  # 1 year

        return response

    def generate_random_promocode(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
