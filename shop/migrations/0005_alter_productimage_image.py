# Generated by Django 5.1.5 on 2025-02-05 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_attribute_options_alter_product_attributes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to='products/', verbose_name='Изображение'),
        ),
    ]
