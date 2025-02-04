from itertools import product

from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from shop.models import Product

def main_page(request: HttpRequest):
    print(f"{request.method=}")
    print(f"{request.content_type=}")
    print(f"{request.GET}")
    product_titles = Product.objects.values_list('title', flat=True)
    titles = b''
    for title in product_titles:
        titles +=title.encode('utf-8')+b"\n"
    print(f"{titles.decode("utf-8")=}")
    return HttpResponse(titles)
