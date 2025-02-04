from django.contrib import admin
from django.contrib import messages

from shop.models import ProductImage, Product, Attribute
from shop.filters import ProductStockFilter


# admin.site.register(Product)
# admin.site.register(ProductImage)
# admin.site.register(Attribute)
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
    search_fields = ('title', 'description')
    list_filter = ('attributes', ProductStockFilter,)
    list_display = ('title', 'price', 'stock')
    actions = (set_zero_stock,)


@admin.register(ProductImage)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('image', 'product')


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)
