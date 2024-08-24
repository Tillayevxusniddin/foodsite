import json

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from .services import *
from config.settings import MEDIA_ROOT
from .forms import *


def home_page(request):
    if request.GET:
        product = get_product_by_id(request.GET.get("product_id", 0))
        return JsonResponse(product)


def order_page(request):
    if request.GET:
        user = get_user_by_phone(request.GET.get("phone_number", 0))
        return JsonResponse(user)


def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    orders = []
    orders_list = request.COOKIES.get("orders")
    total_price = request.COOKIES.get("total_price", 0)
    print(orders_list)
    print(total_price)
    if orders_list:
        for key, val in json.loads(orders_list).items():
            orders.append(
                {
                    "product": Product.objects.get(pk=int(key)),
                    "count": val
                }
            )
    context = {
        'categories': categories,
        'products': products,
        'orders': orders,
        'total_price': total_price,
        'MEDIA_ROOT': MEDIA_ROOT
    }

    response = render(request, 'food/index.html', context)
    response.set_cookie("greeting", "hello")
    # responsega set cookie qilib cookie jonatvorsa boladi
    return response


def main_order(request):
    model = Customer()
    if request.POST:
        try:
            model = Customer.objects.get(phone_number=request.POST.get("phone_number", ""))
        except:
            model = Customer()
        form = CustomerForm(request.POST, instance=model)
        if form.is_valid():
            customer = form.save()  # forma saqlanadi
            formOrder = OrderForm(request.POST, instance=Order()) # Zakaz form yaratiladi
            if formOrder.is_valid():
                order = formOrder.save(customer=customer)
                print("order:",order)
                order_list = request.COOKIES.get("orders")

                for key, value in json.loads(order_list).items():
                    product =get_product_by_id(int(key))

                    counts = value
                    #savat yaratiladi
                    order_product = OrderProduct(
                        count = counts,
                        price = product['price'],
                        product_id = product['id'],
                        order_id = order.id
                    )
                    order_product.save()
                    return redirect("index")
                else:
                    print(formOrder.errors)
            else:
                print(form.errors)

    categories = Category.objects.all()
    products = Product.objects.all()
    orders = []
    orders_list = request.COOKIES.get("orders")
    total_price = request.COOKIES.get("total_price")
    if orders_list:
        for key , val in json.loads(orders_list).items():
            orders.append(
                {
                    "product": Product.objects.get(pk=int(key)),
                    "count": val
                }
            )
    context = {
        'categories': categories,
        'products': products,
        'orders': orders,
        'total_price': total_price,
        'MEDIA_ROOT': MEDIA_ROOT,
    }

    response = render(request, 'food/order.html', context)
    response.set_cookie("greeting","hello")
    return response





