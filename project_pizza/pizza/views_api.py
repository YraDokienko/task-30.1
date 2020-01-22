from django.http import JsonResponse
from django.views import View
from .models import Pizza, Order, InstancePizza


class ApiPizzaView(View):

    def get(self, request):
        sort = request.GET.get('sort')
        pizzas = Pizza.objects.all()
        data = []
        if sort:
            pizzas = pizzas.order_by(sort)
        for pizza in pizzas:
            data.append(pizza.get_serialized_pizza())
        return JsonResponse({"pizza_list": data})


class ApiOrderView(View):

    def get(self, request):
        order = Order.objects.first()
        full_price = order.full_price
        order_pizza = []
        for pizza in order.pizzas.all():
            order_pizza.append({
                "name": pizza.name,
                "count": pizza.count,
                "price": pizza.price,
            })
        return JsonResponse({"order": order_pizza, "full_price": full_price})


class ApiFilterPriceView(View):

    def get(self, request):
        filter_min = request.GET.get('min')
        filter_max = request.GET.get('max')

        data = []
        pizzas = Pizza.objects.filter(price__gt=filter_min, price__lt=filter_max).order_by('price')
        for pizza in pizzas:
            data.append(pizza.get_serialized_pizza())
        return JsonResponse({"pizza_list": data})


class ApiAddPizzaToOrder(View):

    def post(self, request, *args, **kwargs):
        order = Order.objects.first()
        if not order:
            order = Order.objects.create()

        pizza_id = request.GET.get('pizza_id')
        count = request.GET.get('count')
        instance_pizza = InstancePizza.objects.filter(pizza_template=pizza_id)

        if instance_pizza:
            instance_pizza = InstancePizza.objects.get(pizza_template=pizza_id)
            instance_pizza.count += int(count)
            instance_pizza.save()
            order.save_full_price()

        else:
            pizza = Pizza.objects.get(id=pizza_id)
            instance_pizza = InstancePizza.objects.create(
                name=pizza.name,
                size=pizza.size,
                price=pizza.price,
                count=count,
                pizza_template=pizza
            )

            order.pizzas.add(instance_pizza)
            order.save_full_price()
        return JsonResponse({"message": "Pizza add to order!"})
