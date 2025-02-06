from itertools import product

from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from shop.models import Product
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm


def main_page(request: HttpRequest):
    products = Product.objects.all()
    return render(request,
                  'index.html',
                  context={"products": products})


def all_products(request):
    products = Product.objects.all()
    current_time = datetime.now()

    return render(request, 'products.html', {
        'products': products,
        'current_time': current_time
    })

def register_page(request: HttpRequest):
    form = UserCreationForm
    return render(request, 'registration.html',
                  context={"form": form})
