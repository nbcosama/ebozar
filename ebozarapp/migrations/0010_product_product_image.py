# Generated by Django 5.1.2 on 2024-10-23 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebozarapp', '0009_alter_product_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]
