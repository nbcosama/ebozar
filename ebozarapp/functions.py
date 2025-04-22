import smtplib
from email.mime.text import MIMEText
from django.http import JsonResponse
from .models import *
import re
import random, string
from django.db.models import Count
from django.db.models import Count
from itertools import chain

from datetime import timedelta
from django.utils import timezone
from django.core.cache import cache
import logging
logger = logging.getLogger(__name__)



# Function to send email to user
def sendemail(request, email, random_number):
    to_email = email
    random_num = random_number
    def is_valid_email(to_email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", to_email) is not None
    if not is_valid_email(to_email):
        return JsonResponse({"message": "Invalid email format", "mail": "Failed"})
    from_email = "smtp.otp@gmail.com"
    app_password = "emir yxvo wpsr ctuv"
    msg = MIMEText(f"Hi there! This is your verification code {random_num}")
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "Verification Code"
    try:
        connection = smtplib.SMTP("smtp.gmail.com", 587)
        connection.starttls() 
        connection.login(user=from_email, password=app_password)
        connection.sendmail(from_addr=from_email, to_addrs=[to_email], msg=msg.as_string())
        connection.close() 
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"message": "Error", "mail": str(e)})



# Function to send username to user
def send_username(request, email, username):
    to_email = email
    user_name = username
    def is_valid_email(to_email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", to_email) is not None
    if not is_valid_email(to_email):
        return JsonResponse({"message": "Invalid email format", "mail": "Failed"})
    from_email = "smtp.otp@gmail.com"
    app_password = "emir yxvo wpsr ctuv"
    msg = MIMEText(f"Hi there! <strong>{user_name}</strong> is your user name" , "html")
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = "User Name"
    try:
        connection = smtplib.SMTP("smtp.gmail.com", 587)
        connection.starttls() 
        connection.login(user=from_email, password=app_password)
        connection.sendmail(from_addr=from_email, to_addrs=[to_email], msg=msg.as_string())
        connection.close() 
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"message": "Error", "mail": str(e)})
    
    
    




# Function to prepare product data for display
def prepareProduct(products):
    product_data = []
    slugs = Slug.objects.all()
    secondary_image = Secondary_images.objects.all()
        
    for product in products:
        slug =  slugs.filter(prooduct_id=product.id)
        sec_images = secondary_image.filter(product_id=product.id)
        profileverified = VerifiedProfile.objects.filter(profile=product.user).first()
        if not slug:
            product_name = product.product_name
            # Replace spaces with underscores and remove special characters
            product_name_slug = re.sub(r'[^a-zA-Z0-9_]+', '', product_name.replace(" ", "_").replace("/", "")).lower()
            if slugs.filter(product_slug = product_name_slug):
                product_name_slug += str(product.pk)
            slg = Slug(prooduct_id= product.id, product_slug= product_name_slug)
            slg.save()
        data = {
            'product_image'  : product.product_image, 
            'product_name' : product.product_name, 
            'store_name'   : product.user.store_name,
            'price' : product.price,
            'brand' : product.brand,
            'condtion' : product.condtion,
            'quantity' : product.quantity,
            'color' : product.color,
            'slug': slug[0],
            'sec_images': [x.secondary_image.url for x in sec_images],
            'profileverified': profileverified.is_verified if profileverified else False
        }
        product_data.append(data)
    return product_data





# SKU generator function
def generate_sku(product_name, brand, color, description):
    # Convert inputs to uppercase and take the first three characters of each attribute to keep SKU concise
    product_name_part = (product_name[:3] if product_name else "GEN").upper()
    brand_part = (brand[:3] if brand else "UNK").upper()
    color_part = (color[:3] if color else "STD").upper()
    description_part = (''.join(word[0] for word in description.split()[:2]) if description else "KW").upper()
    # Generate a random 4-digit number for uniqueness
    unique_id = ''.join(random.choices(string.digits, k=4))
    # Combine all parts to form the SKU
    sku = f"{product_name_part}-{brand_part}-{color_part}-{description_part}-{unique_id}"
    # remove any spaces
    sku = sku.replace(" ", "")
    return sku








def SaveUserActivity(request, device_id, product_id):
    if not device_id or not product_id:
        return JsonResponse({"message": "Missing required fields", "status": "Failed"})


    cooldown = timezone.now() - timedelta( minutes=1)
    recent_view = UserActivity.objects.filter(
        device_id=device_id,
        product_id=product_id,
        viewed_at__gte=cooldown
    ).exists()


    try:
        if device_id and not recent_view:
            product = Product.objects.get(id=product_id)
            user_activity = UserActivity(device_id=device_id, product=product)
            user_activity.save()
            return JsonResponse({"message": "User activity saved successfully", "status": "Success"})
    except Product.DoesNotExist:
        return JsonResponse({"message": "Product not found", "status": "Failed"})
    except Exception as e:
        return JsonResponse({"message": f"Error: {str(e)}", "status": "Failed"})





def get_recommendations(device_id, limit=10):
    # Get all categories the user viewed, sorted by most viewed
    top_categories = (
        UserActivity.objects.filter(device_id=device_id)
        .values('product__product_category')
        .annotate(view_count=Count('product'))
        .order_by('-view_count')
    )

    viewed_product_ids = set(
        UserActivity.objects.filter(device_id=device_id)
        .values_list('product_id', flat=True)
    )

    
    recommended_products = []
    for category in top_categories:
        category_id = category['product__product_category']
        
        # Randomize products within category, exclude already viewed
        products = Product.objects.filter(product_category_id=category_id).order_by('?')[:limit]

        for product in products:
            if product.id not in [p.id for p in recommended_products]:
                recommended_products.append(product)
                if len(recommended_products) >= limit:
                    break

        if len(recommended_products) >= limit:
            break

    # Fallback: fill with random products if limit not reached
    if len(recommended_products) < limit:
        needed = limit - len(recommended_products)
        fallback = Product.objects.exclude(id__in=[p.id for p in recommended_products]).order_by('?')[:needed]
        recommended_products = list(chain(recommended_products, fallback))

    return recommended_products
