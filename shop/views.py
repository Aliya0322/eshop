from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views import View


from shop.models import Product
from datetime import datetime
from shop.forms import CustomUserCreationForm, UserAuthForm



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
            username = form.cleaned_data['username']  # Используем [] для доступа к данным
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
