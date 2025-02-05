import uuid

from django.db import models
from django.contrib.auth.models import User


class ProductManager(models.Manager):
    def in_stock(self):
        return self.get_queryset().filter(stock__gt=0)

    def order_by_price_desc(self):
        return self.get_queryset().order_by('-price')

    def order_by_price_asc(self):
        return self.get_queryset().order_by('price')


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.FloatField(verbose_name='Цена')
    stock = models.IntegerField(verbose_name='В наличии')
    attributes = models.ManyToManyField('Attribute', verbose_name='Свойства')

    objects = ProductManager()

    def __str__(self):
        return f"{self.title}: #{self.id}"


    class Meta:
        indexes = [models.Index(fields=['title']),
                   models.Index(fields=['price'])]
        db_table = 'product'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class ProductImage(models.Model):
    image = models.ImageField(upload_to="products/", verbose_name="Изображение")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображение товаров'


class Attribute(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Свойство'
        verbose_name_plural = 'Свойства'


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
