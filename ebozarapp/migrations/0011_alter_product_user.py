# Generated by Django 5.1.2 on 2024-10-23 16:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebozarapp', '0010_product_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ebozarapp.profile'),
        ),
    ]
