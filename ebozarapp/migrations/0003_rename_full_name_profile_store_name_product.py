# Generated by Django 5.1.2 on 2024-10-20 08:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebozarapp', '0002_profile_full_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='full_name',
            new_name='store_name',
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('price', models.CharField(max_length=10)),
                ('brand', models.CharField(max_length=50)),
                ('condtion', models.CharField(max_length=50)),
                ('quantity', models.CharField(max_length=5)),
                ('color', models.CharField(max_length=100)),
                ('Location', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
