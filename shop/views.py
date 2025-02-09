from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DetailView


from shop.models import Product
from datetime import datetime
from shop.forms import CustomUserCreationForm, UserAuthForm


class MainView(ListView):
    template_name = 'index.html'
    model = Product
    context_object_name = 'products'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.prefetch_related("productimage_set")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["is_authenticated"] = self.request.user.is_authenticated
        return data


class AllProductsView(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = datetime.now()
        return context


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


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

    def get_object(self):
        qs=super().get_queryset()
        return qs.prefetch_related("productimage_set")