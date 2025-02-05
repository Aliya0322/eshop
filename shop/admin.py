from django.contrib import admin
from django.contrib import messages
from django.contrib.admin import TabularInline

from shop.models import ProductImage, Product, Attribute
from shop.filters import ProductStockFilter


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.action(description='Обнулить остатки')
def set_zero_stock(modeladmin, request, queryset):
    queryset.update(stock=0)
    modeladmin.message_user(
        request,
        "Остатки товаров обнулены.",
        level=messages.SUCCESS
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    search_fields = ('title', 'description')
    list_filter = ('attributes', ProductStockFilter,)
    list_display = ('title', 'price', 'stock')
    actions = (set_zero_stock,)


@admin.register(ProductImage)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'product')


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)
