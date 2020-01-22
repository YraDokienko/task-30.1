from django.urls import path
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from . import views, views_api
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', cache_page(20*1)(views.PizzaHomeView.as_view()), name='home'),
    path('pizza-form-add/', views.PizzaFormAddView.as_view(), name='pizza_add'),
    path('cart/', views.PizzaCartView.as_view(), name='cart'),
    path('stop_spam_page/', TemplateView.as_view(template_name='stop_spam_page.html')),
    path('pizza-price-update/', views.PizzaPriceUpdateView.as_view(), name='price_update'),
    path('add-pizza-to-order/', views.AddPizzaToOrderView.as_view()),
    path('cart/shipping/', views.ShippingOrderView.as_view(), name='shipping'),
    path('cart/shipping/create/', views.HomePageCreateOrder.as_view(), name='create'),
    path('del_instance/<int:id>', views.AddPizzaToOrderView.del_instance, name='delete'),
    path('pizza-update/<int:pk>/edit/', views.PizzaUpdateView.as_view(), name='pizza_update'),
    path('api/all_pizza/', views_api.ApiPizzaView.as_view(), name='api_pizzas'),
    path('api/filter_price/', views_api.ApiFilterPriceView.as_view(), name='api_filter_price'),
    path('api/add_pizza_order/', views_api.ApiAddPizzaToOrder.as_view(), name='api_add_pizza_order'),
    path('api/order/', views_api.ApiOrderView.as_view(), name='api_order'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
