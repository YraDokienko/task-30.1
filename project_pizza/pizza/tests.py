from django.test import TestCase
from django.urls import resolve, reverse
from .forms import ShippingOrderForm


class PizzaTestCase(TestCase):

    def setUp(self) -> None:
        pass

    def test_page_pizza_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pizza_home.html')
        self.assertContains(response, 'АМЕРИКАНО')

    def test_page_pizza_form_add(self):
        response = self.client.get('/pizza-form-add/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form_pizza_add.html')

    def test_page_pizza_price_update(self):
        response = self.client.get('/pizza-price-update/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pizza_price_update.html')

    def test_page_pizza_edit(self):
        url = reverse('pizza_update', args=[75])
        self.assertEqual(url, '/pizza-update/75/edit/')
        resol = resolve(url)
        self.assertEqual(resol.view_name, 'pizza_update')


class ShippingTestCase(TestCase):

    def setUp(self) -> None:
        pass

    def test_page_shipping(self):
        response = self.client.get('/cart/shipping/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shipping.html')

    # Valid Form
    def test_shipping_form_valid(self):

        form = ShippingOrderForm(data={
            "first_name": 'Vova', "last_name": 'Petrenko', "email": 'r@gmail.com',
            "phone": 380501234567, "city": 'Odessa', "street": 'Torgova', "house": '20',
            "apartment": '13', "front_door": 1, "floor": 5, "number_persons": 5,
            "comment": 'go to', "type_payment": 'card',
        })
        self.assertTrue(form.is_valid())

    # Invalid Form
    def test_shipping_form_invalid(self):

        form = ShippingOrderForm(data={
            "first_name": 'Vova', "last_name": 'Petrenko', "email": ' ',
            "phone": 'ERROR', "city": 'Odessa', "street": 'Torgova', "house": '20',
            "apartment": '13', "front_door": 1, "floor": 5, "number_persons": 5,
            "comment": 'go to', "type_payment": 'card',
        })
        self.assertFalse(form.is_valid())