from django.contrib import admin
from .models import Pizza, Size, Ingredient, Order, InstancePizza, ShippingOrder


class PizzaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['id', 'name', 'size', 'price', 'available']
    list_display_links = ['name']
    list_editable = ['price']
    list_filter = ['size', 'price']
    search_fields = ['^name']


class IngredientAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price']
    list_display_links = ['name']
    list_editable = ['price']
    list_filter = ['price']


class InstancePizzaAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'size', 'price', 'count']
    list_editable = ['price', 'count']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_price']


class ShippingOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'phone', 'email', 'city',
                    'street', 'house', 'apartment', 'front_door', 'floor',
                    'number_persons', 'created', 'type_payment', 'comment']


admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Size)
admin.site.register(Order, OrderAdmin)
admin.site.register(InstancePizza, InstancePizzaAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(ShippingOrder, ShippingOrderAdmin)

