from .models import Order, Pizza


def context_pizza(request):
    return {
        'pizzas': Pizza.objects.all(),
        'order': Order.objects.first(),
    }
