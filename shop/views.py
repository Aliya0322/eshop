import json


from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.db.models import F, QuerySet, Value
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from shop.models import Product
from datetime import datetime
from shop.forms import CustomUserCreationForm, UserAuthForm
from shop.mixins import IsAuthenticatedMixin


class MainView(IsAuthenticatedMixin, ListView):
    template_name = 'index.html'
    model = Product
    context_object_name = 'products'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.prefetch_related("productimage_set")


class AllProductsView(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = datetime.now()
        return context


@method_decorator(ensure_csrf_cookie, name="dispatch")
class RegistrationView(View):
    @staticmethod
    def get(request: HttpRequest):
        form = CustomUserCreationForm()
        return render(request, 'registration.html', context={"form": form})

    @staticmethod
    def post(request: HttpRequest):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("all-products")
        return render(request, 'registration.html', context={"form": form})


class LoginView(View):
    @staticmethod
    def get(request: HttpRequest):
        form = UserAuthForm()
        return render(request, "login.html", context={'form': form})

    @staticmethod
    def post(request: HttpRequest):
        form = UserAuthForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('main-page')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль')
        else:
            messages.error(request, form.errors)

        form = UserAuthForm()
        return render(request, "login.html", context={'form': form})


def logout_user(request: HttpRequest):
    logout(request)
    return redirect('main-page')


@method_decorator(ensure_csrf_cookie, name="dispatch")
class ProductDetailView(IsAuthenticatedMixin, DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        qs = super().get_queryset()
        discount = 100
        increase = 100

        if self.request.user.is_authenticated:
            qs = qs.annotate(
                discount_price=F("price") - Value(discount)
            )
        else:
            qs = qs.annotate(
                increased_price=F("price") + Value(increase)
            )

        return qs.prefetch_related("productimage_set")

    def get_context_data(self, **kwargs):
        cd = super().get_context_data(**kwargs)
        cd["discount"] = self.request.discount
        return cd


class CartView(View):
    @staticmethod
    def get(request: HttpRequest, product_id: int):
        cart = request.session.get("cart", {})

        if not cart:
            return JsonResponse({"detail": "Cart is empty"}, status=404)

        if str(product_id) not in cart:
            return JsonResponse({"detail": "Product not found in cart"}, status=404)

        return JsonResponse({"quantity": cart[str(product_id)]}, status=200)

    @staticmethod
    def post(request: HttpRequest):
        try:
            data = json.loads(request.body.decode('utf-8'))
            product_id = str(data["productId"])
            quantity = int(data["quantity"])

            cart = request.session.get("cart", {})
            if product_id in cart:
                cart[product_id] += quantity
            else:
                cart[product_id] = quantity

            request.session["cart"] = cart
            return JsonResponse({"success": True}, status=200)

        except (KeyError, ValueError, json.JSONDecodeError) as e:
            return JsonResponse({"error": str(e)}, status=400)

    @staticmethod
    def delete(request: HttpRequest, product_id: int):
        cart = request.session.get("cart")

        if not cart:
            return JsonResponse({"detail": "Cart is empty"}, status=404)

        product_id = str(product_id)
        if product_id not in cart:
            return JsonResponse({"detail": "Product not found in cart"}, status=404)

        del cart[product_id]
        request.session.update({"cart": cart})
        return JsonResponse({}, status=204)


class ShowCartView(View):
    def get(self, request: HttpRequest):
        cart = request.session.get("cart", {})

        if not cart:
            return JsonResponse({"detail": "Cart is empty"}, status=404)

        product_ids = cart.keys()
        discount = 100
        increase = 100

        products = Product.objects.filter(id__in=product_ids).annotate(
            discount_price=F("price") - Value(discount),
            increased_price=F("price") + Value(increase)
        )

        if request.user.is_authenticated:
            product_quantity_cart = {
                product: (
                    cart.get(str(product.id), 0),
                    cart.get(str(product.id), 0) * product.discount_price)
                for product in products
            }

        else:
            product_quantity_cart = {
                product: (
                    cart.get(str(product.id), 0),
                    cart.get(str(product.id), 0) * (product.increased_price)
                )
                for product in products
            }

        total_sum = sum(quantity_price[1] for quantity_price in product_quantity_cart.values())

        return render(request, "show_cart.html", context={
            "cart": product_quantity_cart,
            "discount": discount if request.user.is_authenticated else 0,
            "total_sum": total_sum
        })
