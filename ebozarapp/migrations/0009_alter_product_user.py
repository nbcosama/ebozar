# Generated by Django 5.1.2 on 2024-10-23 14:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ebozarapp', '0008_remove_otp_user_otp_email_otp_json_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='ebozarapp.profile'),
        ),
    ]
