from .forms import PizzaForm, PizzaPriceUpdateForm, PizzaSortedForm, \
    AddPizzaToOrderForm, ShippingOrderForm
from django.views.generic import ListView, FormView, UpdateView, TemplateView
from django.http import HttpResponseRedirect
from .models import Pizza, Order, InstancePizza


class PizzaHomeView(ListView):
    model = Pizza
    template_name = 'home.html'

    def get_queryset(self):
        sort = self.request.GET.get('sort_order', 'name')
        return Pizza.objects.all().order_by(sort)

    def get_context_data(self,  *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = Pizza.objects.all().count()
        context['list'] = Pizza.objects.values_list('name', flat=True)
        context['form'] = PizzaSortedForm
        return context


class PizzaFormAddView(FormView):
    template_name = 'form_pizza_add.html'
    form_class = PizzaForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class PizzaUpdateView(UpdateView):
    form_class = PizzaForm
    model = Pizza
    template_name = 'form_pizza_add.html'
    success_url = '/'


class PizzaPriceUpdateView(FormView):
    template_name = 'pizza_price_update.html'
    form_class = PizzaPriceUpdateForm
    success_url = '/'

    def form_valid(self, form):
        value = form.cleaned_data
        pizzas = Pizza.objects.all()
        for pizza in pizzas:
            pizza.price = pizza.price + value['value']
            pizza.save()
        return super().form_valid(form)


class AddPizzaToOrderView(FormView):
    form_class = AddPizzaToOrderForm
    success_url = '/'

    def form_valid(self, form):
        order = Order.objects.first()
        if not order:
            order = Order.objects.create()

        pizza_id = form.cleaned_data.get('pizza_id')
        instance_pizza = InstancePizza.objects.filter(pizza_template=pizza_id)

        if instance_pizza:
            instance_pizza = InstancePizza.objects.get(pizza_template=pizza_id)
            count = form.cleaned_data.get('count')
            instance_pizza.count += count
            instance_pizza.save()

        else:
            count = form.cleaned_data.get('count')
            pizza_id = form.cleaned_data.get('pizza_id')
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
        return super().form_valid(form)

    def del_instance(self, id):
        order = Order.objects.first()
        instance = InstancePizza.objects.get(id=id)
        instance.delete()
        order.save_full_price()
        return HttpResponseRedirect("/cart")


class PizzaCartView(TemplateView):
    template_name = 'cart.html'


class ShippingOrderView(FormView):
    template_name = 'shipping.html'
    form_class = ShippingOrderForm
    success_url = 'create/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ShippingOrderView, self).get_context_data(**kwargs)
        context['order'] = Order.objects.first()
        return context


class HomePageCreateOrder(TemplateView):

    template_name = 'created.html'
