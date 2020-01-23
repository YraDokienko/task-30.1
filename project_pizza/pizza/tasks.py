from .models import InstancePizza, Pizza, Order
from project_pizza.celery import app
from bs4 import BeautifulSoup
import requests

URL = 'https://vilki-palki.od.ua/pizza'
DATA = []


@app.task(name='parser_site_pizza')
def parser_site_pizza():
    response = requests.get(URL)
    contents = response.text
    soup = BeautifulSoup(contents, 'lxml')
    div = soup.find_all("div", {"class": "item"})
    for row in div:
        price_all = row.find_all("span", {"class": "day"})
        name_all = row.find_all("div", {"class": "name fl2"})
        description_all = row.find_all("div", {"class": "cont-text fl1"})
        image_url_all = row.find_all("div", {"class": "img"})

        price = price_all[0].span.contents[0]
        name = name_all[0].a.contents[0].strip()
        description = description_all[0].contents[0].rstrip()
        image_url = "https://vilki-palki.od.ua/" + image_url_all[0].img.attrs["src"]

        DATA.append({
            name: {
                "name": name,
                "price": price,
                "description": description,
                "image_url": image_url,
            }
        })

    for item in DATA:
        print(item)


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
