from .models import InstancePizza, Pizza, Order
from project_pizza.celery import app


@app.task(name="add_pizza_to_card")
def add_pizza_to_cart(pizza_id, count):
    order = Order.objects.first()
    if not order:
        order = Order.objects.create()
    instance_pizza = InstancePizza.objects.filter(pizza_template=pizza_id)

    if instance_pizza:
        instance_pizza = InstancePizza.objects.get(pizza_template=pizza_id)
        instance_pizza.count += count
        instance_pizza.save()

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
    print("Add pizza_id = {} to cart ".format(pizza_id))


