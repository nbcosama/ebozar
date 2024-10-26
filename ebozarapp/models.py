from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone




class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=30)
    bio = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to='media/', null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    verify  = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)
    date_time = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    

    def __str__(self):
        return self.user.username


class Product(models.Model):
    product_image = models.ImageField(upload_to='media/', null=True, blank=True)
    product_name = models.CharField(max_length=255)
    price = models.CharField(max_length=10)
    brand = models.CharField(max_length=50)
    condtion = models.CharField(max_length=50)
    quantity = models.CharField(max_length=5)
    color = models.CharField(max_length=100)
    Location = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
   
    def __str__(self):
        return self.product_name
    
    


class OTP(models.Model):
    email = models.EmailField(max_length=254)
    otp = models.CharField(max_length=6)
    json_data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # OTP is valid for 5 minutes
        return timezone.now() < self.created_at + datetime.timedelta(minutes=5)

    def __str__(self):
        return self.email