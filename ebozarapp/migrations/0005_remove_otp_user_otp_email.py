# Generated by Django 5.1.2 on 2024-10-20 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebozarapp', '0004_otp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otp',
            name='user',
        ),
        migrations.AddField(
            model_name='otp',
            name='email',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
