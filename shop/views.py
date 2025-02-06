from itertools import product

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from shop.models import Product
from datetime import datetime
from shop.forms import CustomUserCreationForm



def main_page(request: HttpRequest):
    products = Product.objects.all()
    return render(request,
                  'index.html',
                  context={"products": products, "is_authenticated": request.user.is_authenticated})


def all_products(request):
    products = Product.objects.all()
    current_time = datetime.now()

    return render(request, 'products.html', {
        'products': products,
        'current_time': current_time
    })

def register_page(request: HttpRequest):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("main-page")
    form = CustomUserCreationForm
    return render(request, 'registration.html',
                  context={"form": form})
