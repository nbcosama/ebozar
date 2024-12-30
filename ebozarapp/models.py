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
    facebook = models.CharField(max_length=200, null=True, default="")
    instagram = models.CharField(max_length=200, null=True, default="")
    morelink = models.CharField(max_length=200, null=True, default="")
    store_timing = models.CharField(max_length=255, null=True, blank=True, default="Not Set")
    logo = models.ImageField(upload_to='media/', null=True, blank=True)
    profilePic = models.ImageField(upload_to='media/', null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    verify  = models.BooleanField(default=True)
    latitude = models.CharField(max_length=100, default="")
    longitude = models.CharField(max_length=100, default="")
    date = models.DateField(auto_now_add=True)
    date_time = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    

    def __str__(self):
        return self.user.username


class ProductCategories(models.Model):
    category_name = models.CharField( max_length=100)
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.category_name



class Product(models.Model):
    product_category = models.ForeignKey(ProductCategories, on_delete=models.CASCADE, null=True, default="")
    product_image = models.ImageField(upload_to='media/', null=True, blank=True)
    product_name = models.CharField(max_length=255, db_index=True)
    price = models.CharField(max_length=10)
    brand = models.CharField(max_length=50)
    condtion = models.CharField(max_length=50)
    discount = models.CharField(max_length=50, default="")
    quantity = models.CharField(max_length=10)
    color = models.CharField(max_length=100)
    sku = models.CharField(max_length=255, default="")
    product_description = models.CharField(max_length=255, default="Enter Key")
    status = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
   
    def __str__(self):
        return self.product_name
    


class Secondary_images(models.Model):
    secondary_image = models.ImageField(upload_to='media/', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    def __str__(self):
        return self.product.product_name



class Slug(models.Model):
    prooduct = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_slug = models.CharField(max_length=255)

    def __str__(self):
        return self.product_slug


    


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
    



class Searched_Query(models.Model):
    query = models.CharField(max_length=255, db_index=True)
    ip_address = models.CharField(max_length=255 , null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    date_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.query
    





class buyerCart(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    dateTime = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.product.product_name




class buyerOrder(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="buyer")
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="seller", null=True, blank=True)
    orderStatus = models.CharField(max_length=100, default="Pending")
    date = models.DateField(auto_now_add=True)
    dateTime = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.user.username
    


class buyerProducts(models.Model):
    order = models.ForeignKey(buyerOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=10)
    totalAmount = models.CharField(max_length=10, default=0)
    dateTime = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.product.product_name