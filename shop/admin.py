from django.contrib import admin

from shop.models import (ProductImage, Product, Attribute)


# admin.site.register(Product)
# admin.site.register(ProductImage)
# admin.site.register(Attribute)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock')


@admin.register(ProductImage)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('image', 'product')


@admin.register(Attribute)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)
