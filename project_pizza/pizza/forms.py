from django.forms import ModelForm
from django import forms
from .models import Pizza, ShippingOrder


class PizzaForm(ModelForm):
    class Meta:
        model = Pizza
        fields = ['name', 'price', 'size', 'description', 'available',
                  'ingredient']


class PizzaPriceUpdateForm(forms.Form):
    value = forms.DecimalField(max_digits=7, decimal_places=2)

    def create_object(self):
        Pizza.objects.create(
            value=self.cleaned_data.get('value'),
        )


class PizzaSortedForm(forms.Form):
    sort_order = forms.ChoiceField(
        label='Сортировка',
        required=False,
        choices=[
            ['name', 'по алфавиту'],
            ['price', 'цена по возрастанию'],
            ['-price', 'цена по убыванию'],
        ])


class AddPizzaToOrderForm(forms.Form):
    count = forms.IntegerField()
    pizza_id = forms.IntegerField()


class ShippingOrderForm(ModelForm):
    apartment = forms.CharField(required=False)
    front_door = forms.ImageField(required=False)
    floor = forms.ImageField(required=False)
    comment = forms.CharField(required=False)
    type_payment = forms.ChoiceField(required=False, choices=[
        ['cash', 'Наличными при получении'],
        ['card', 'Оплата картой']
    ])

    class Meta:
        model = ShippingOrder
        fields = ['first_name', 'last_name', 'email', 'phone', 'city',
                  'street', 'house', 'apartment', 'front_door',
                  'floor', 'number_persons', 'type_payment', 'comment', ]
