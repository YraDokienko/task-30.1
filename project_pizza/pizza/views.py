from .forms import PizzaForm, PizzaPriceUpdateForm, PizzaSortedForm, \
    AddPizzaToOrderForm, ShippingOrderForm
from django.views.generic import ListView, FormView, UpdateView, TemplateView
from django.http import HttpResponseRedirect
from .models import Pizza, Order, InstancePizza
from .tasks import add_pizza_to_cart, parser_site_pizza


class PizzaHomeView(ListView):
    model = Pizza
    template_name = 'home.html'

    def get_queryset(self):
        parser_site_pizza.apply_async(countdown=1 * 60)
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
        pizza_id = form.cleaned_data.get('pizza_id')
        count = form.cleaned_data.get('count')
        add_pizza_to_cart.delay(pizza_id, count)
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
