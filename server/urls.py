"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path

from shop.views import (MainView,
                        AllProductsView,
                        LoginView,
                        logout_user,
                        RegistrationView,
                        ProductDetailView,
                        CartView,
                        ShowCartView)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name='main-page'),
    path('products/', AllProductsView.as_view(), name='all-products'),
    path('register/', RegistrationView.as_view(), name='registration-view'),
    path('login/', LoginView.as_view(), name='login-page'),
    path('logout/', logout_user, name='logout-page'),
    path('products/<int:pk>', ProductDetailView.as_view(), name='product-detail'),
    path('cart/', CartView.as_view(), name="cart"),
    path('cart/<int:product_id>/', CartView.as_view(), name="cart"),
    path('showcart/', ShowCartView.as_view(), name="showcart")

]


if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)