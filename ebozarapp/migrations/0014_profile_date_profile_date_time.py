# Generated by Django 5.1.2 on 2024-10-24 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebozarapp', '0013_product_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='date',
            field=models.DateField(auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=False,
        ),
    ]
