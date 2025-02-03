from django.contrib import admin

from shop.models import (ProductImage, Product, Attribute)


# admin.site.register(Product)
# admin.site.register(ProductImage)
# admin.site.register(Attribute)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'stock', 'images', 'get_attributes')

    @admin.display(description="Изображение товара")
    def images(self, obj: Product):
        return list(obj.productimage_set.values_list('image', flat=True))

    @admin.display(description="Свойства")
    def get_attributes(self, obj: Product):
        return list(obj.attributes.values_list('name', flat=True))

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('productimage_set')


@admin.register(ProductImage)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('image', 'product')


@admin.register(Attribute)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)
