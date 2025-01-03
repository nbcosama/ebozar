import json
import random
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from .functions import *
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
import re
from .ai import *
from django.core.paginator import Paginator
from django.utils.crypto import get_random_string


def custom_404_view(request, exception):
    return render(request, '404_error.html', status=404)


def ebazaar_support(request):
    return render(request, 'support.html')


def became_a_seller(request):
    user = str(request.user)
    context = {'user': user}
    return render(request, 'become_a_seller.html', context)


def getDirection(request):
    user = request.user
    if not user.is_authenticated:
        messages.error(request, 'Please login to add or buy product')
        return redirect('login')
    longitude = request.GET.get('longitude')
    latitude = request.GET.get('latitude')
    buyerID = request.GET.get('buyerID')
    buyer = Profile.objects.get(id=buyerID)
    deliveryBoy = Profile.objects.get(user=user)
    context = {'longitude': longitude, 'latitude': latitude, 'buyer': buyer, 'deliveryBoy': deliveryBoy}
    return render(request, 'direction.html', context)


def landingpage(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category')
    product_category = request.GET.get('product_category')
    location = request.GET.get('location')
    resp_list = []
    if query.strip():
        # resp_list =get_search_results(query)
        if not Searched_Query.objects.filter(query=query).exists():
            searched_query = Searched_Query(query=query)
            searched_query.save() 
        products = Product.objects.filter(
        Q(product_name__icontains=query) |
        Q(product_description__icontains=query) |
        Q(brand__icontains=query) |
        Q(color__icontains=query) |
        Q(sku__icontains=query)
         ).order_by("-id")
    elif product_category:
        if location:
            products = Product.objects.filter(product_category=product_category, user__city = location).order_by("-id")

        products = Product.objects.filter(product_category=product_category).order_by("-id")
    else:
        if location:
            
            products = Product.objects.filter(user__city = location).order_by("-id")
        else:
            products = Product.objects.all().order_by("-id")
    user = str(request.user)
    stores = Profile.objects.filter(verify=True)
    # products = Product.objects.filter(id__in=resp_list).order_by("-id") if query else Product.objects.all().order_by("-id")
    product_data = prepareProduct(products)
    # pegination
    paginator = Paginator(product_data, 30)  # Show 10 products per page
    page_number = request.GET.get('page')
    product_dat = paginator.get_page(page_number)
    product_category = ProductCategories.objects.all()
    context = {'products': product_dat, 'query': query, 'stores': stores, 'category':category, 'product_category':product_category, 'user' :user}
    if request.GET.get("format") == "json":
        return JsonResponse(product_data, safe=False)
    return render(request, 'landingpage.html', context)






def login(request):
    user = request.user
    if user.is_authenticated:
        user_profile = Profile.objects.get(user=user)
        if user_profile.user_type == 'seller':
            return redirect('dashboard')
        return redirect('customerOrders')

    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            if not username or not password:
                messages.error(request, 'Username and password are required.')
                return redirect('login')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                verified_user = Profile.objects.get(user=user)
                auth_login(request, user)
                messages.success(request, 'Logged In successfully')
                if verified_user.user_type == 'seller':
                    return redirect('dashboard')
                return redirect('customerOrders')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('login')
    return render(request, 'login.html')







def logout(request):
    auth_logout(request)
    messages.success(request, 'Logged Out successfully')
    return redirect('login')








def signup(request):
    if request.user.is_authenticated:
        messages.error(request, 'You are already logged in. please logout to create a new account')
        if request.user.profile.user_type == 'buyer':
            return redirect('customerOrders')
        return redirect('dashboard')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        store_name = request.POST.get('store_name')
        phone_number = request.POST.get('phone_number')
        logo = request.FILES.get('logo')
        address = request.POST.get('address')
        country = request.POST.get('country')
        city = request.POST.get('city')
        longitude = request.POST.get('longitude')
        latitude = request.POST.get('latitude')
        user_type = request.POST.get('user_type')
        if user_type == 'seller' or user_type == 'buyer':
            pass
        else:
            messages.error(request, 'Invalid user type')
            return redirect('signup')
        if not email or not password or not store_name or not phone_number or not address or not country or not city or not user_type:
            messages.error(request, 'All fields are required')
            return redirect('signup')
        user_data = {
            "email": email,
            "password": password, 
            "store_name": store_name,
            "phone_number": phone_number,
            "logo": logo.name if logo else None, 
            "address": address,
            "country": country,
            "city": city,
            "user_type": user_type,
            "latitude": latitude,
            "longitude": longitude
        }
        user_data_json = json.dumps(user_data)
        username = store_name.replace(" ", "_").lower()
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use.')
            return redirect('become-a-seller')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')
        random_number = random.randint(1000, 9999)
        send_otp = sendemail(request, email, random_number)
        save_otp = OTP(otp = random_number, email = email, json_data = user_data_json )
        save_otp.save()
        context = {'email':email}
        return render(request, 'verify_otp.html', context)
    return render(request, 'signup.html')








def verify_otp(request):
    user = request.user
    if user.is_authenticated:
        messages.error(request, 'Invalid request')
        return redirect('dashboard')
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            otp = request.POST.get('otp')
            otp_record = OTP.objects.get(email=email, otp=otp)
            if otp_record.is_valid():
                messages.success(request, 'OTP verified successfully! Your username has been sent to your email.' )
                store_data = OTP.objects.get(email=email, otp=otp)
                data = json.loads(store_data.json_data)
                otp_record.delete()  # Remove the OTP after successful verification
                emails = data['email']
                password = data['password']
                store_name = data['store_name']
                phone_number = data['phone_number']
                # logo = data['logo']
                address = data['address']
                country = data['country']
                city = data['city']
                longitude = data['longitude']
                latitude = data['latitude']
                user_type = data['user_type']
                username = store_name.replace(" ", "").lower()
                user = User(username=username, email=emails)
                user.set_password(password) 
                user.save()
                send_username(request, emails, username)
                profile = Profile(
                        user=user, 
                        store_name=store_name, 
                        phone_number=phone_number, 
                        # logo=logo,
                        address=address, 
                        country=country, 
                        city=city, 
                        user_type=user_type,
                        email = emails,
                        longitude = longitude,
                        latitude = latitude
                    )
                profile.save()
                # Automatically log in the user after signing up
                auth_login(request, user)  
                messages.success(request, 'Account created successfully! Please update your profile')
                if user_type == 'buyer':
                    return redirect('customerOrders')
                return redirect('dashboard')
            
            else:
                messages.error(request, 'OTP has expired or is invalid.')
        except OTP.DoesNotExist:
            message = "Invalid OTP please try again."
            context = { 'email': email, 'messages': message}
            return render(request, 'verify_otp.html', context)
        except Exception as e:
            message = str(e)
            context = { 'email': email, 'messages': message}
            return render(request, 'verify_otp.html', context)
    return render(request, 'verify_otp.html')









@login_required(login_url='/login')
def dashboard(request):
    user = request.user
    if request.method == 'POST':
        if request.GET.get("action") == "update_product":
            product_id = request.GET.get('id')
            product = Product.objects.get(id=product_id)
            if product.status == True:
                product.status = False
                product.save()
                return redirect('dashboard')
            elif product.status == False:
                product.status = True
                product.save()
                return redirect('dashboard')
        if request.GET.get("action") == "delete_product":
            product_id = request.GET.get('id')
            product = Product.objects.get(id=product_id)
            product.delete()
            messages.error(request, 'Product deleted successfully')
            return redirect('dashboard')
    user_profile = Profile.objects.get(user=user)
    user_product = Product.objects.filter(user=user_profile).order_by('-id')
    context = {'user_profile': user_profile, 'user_products': user_product}
    return render(request, 'dashboard.html', context)







@login_required(login_url='/login')
def add_product(request):
    if request.method == 'POST':
        user = request.user
        user_profile = Profile.objects.get(user=user)
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        condtion = request.POST.get('condtion')
        brand = request.POST.get('brand')
        color = request.POST.get('color')
        category = request.POST.get('category')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity')
        discount = request.POST.get('discount')
        product_image = request.FILES.get('compressedFile')
        product_images = request.FILES.getlist('secondaryimages')
        if not product_name or not price or not condtion or not quantity or not product_image:
            return JsonResponse({"message":'All fields are required', "status": "error" })
        if user_profile.verify == False:
            return JsonResponse({"message": 'Please verify your account to add product. To verify account contact support team', "error": "sucess" })
        slugs = Slug.objects.all()

        # Generate SKU
        sku = generate_sku(product_name, brand, color, description)
        product = Product(
            user=user_profile, 
            product_name=product_name, 
            price=price,
            condtion=condtion, 
            product_image=product_image, 
            brand=brand, 
            color=color, 
            product_category_id = category,
            product_description = description,
            sku = sku,
            discount = discount,
            quantity=quantity
            )
        product.save()
        product_name = product.product_name
        
        # Replace spaces with underscores and remove special characters
        product_name_slug = re.sub(r'[^a-zA-Z0-9_]+', '', product_name.replace(" ", "-").replace("/", "")).lower()
        if slugs.filter(product_slug = product_name_slug):
            product_name_slug += str(product.pk)
        add_product_slug = Slug(
            prooduct_id = product.pk,
            product_slug = product_name_slug
        )
        add_product_slug.save()

        for secondary_image in product_images:
            image = secondary_image
            secondary_img = Secondary_images(
            secondary_image=image, 
            product_id = product.pk
            )
            secondary_img.save()
        messages.success(request, 'Product added successfully')
        return JsonResponse({"message":'Product added successfully', "status": "sucess" })
    user = request.user
    product_category = ProductCategories.objects.all()
    user_profile = Profile.objects.get(user=user)
    context = {'user_profile': user_profile, 'product_category':product_category}
    return render(request, 'add_product.html', context)









@login_required(login_url='/login')
def update_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        condtion = request.POST.get('condtion')
        brand = request.POST.get('brand')
        color = request.POST.get('color')
        category = request.POST.get('category')
        key_words = request.POST.get('key_words')
        quantity = request.POST.get('quantity')
        discount = request.POST.get('discount')
        product_image = request.FILES.get('image')
        product.product_name = product_name
        product.price = price
        product.condtion = condtion
        product.brand = brand
        product.color = color
        product.discount = discount
        product.product_category_id = category
        product.product_description = key_words
        product.quantity = quantity
        if product_image:
            product.product_image = product_image
        product.save()
        messages.success(request, 'Product updated successfully')
        return redirect('dashboard')
    id = request.GET.get('product_id')
    user = request.user
    product_category = ProductCategories.objects.all()
    user_profile = Profile.objects.get(user=user)
    product = Product.objects.get(id=id)
    context = {'user_profile':user_profile, 'product': product, 'product_category':product_category}
    return render(request, 'update_product.html', context)











@login_required(login_url='/login')
def profile(request):
    if request.method == 'POST':
        if request.GET.get("action") == "update_profile":
            user = request.user
            user_profile = Profile.objects.get(user=user)
            phone_number = request.POST.get('phone_number')
            address = request.POST.get('address')
            bio = request.POST.get('bio')
            facebook = request.POST.get('facebook')
            instagram = request.POST.get('instagram')
            morelink = request.POST.get('morelink')
            store_timing = request.POST.get('store_timing')
            user_profile.store_timing = store_timing
            user_profile.phone_number = phone_number
            user_profile.address = address
            user_profile.bio = bio
            user_profile.facebook = facebook
            user_profile.instagram = instagram
            user_profile.morelink = morelink
            user_profile.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
        elif request.GET.get("action") == "update_logo":
            user = request.user
            user_profile = Profile.objects.get(user=user)
            logo = request.FILES.get('logo')
            user_profile.logo = logo
            user_profile.save()
            messages.success(request, 'Logo updated successfully')
            return redirect('profile')
            
    user = request.user
    user_profile = Profile.objects.get(user=user)
    context = {'user_profile': user_profile}
    return render(request, 'profile.html', context)






def preview(request, slug):
    user = str(request.user)
    profile = 'buyer'
    if not user == 'AnonymousUser':
        profile = Profile.objects.get(user=request.user)
        print(profile.user_type)
    slug = Slug.objects.filter(product_slug=slug)
    if not slug:
        return render(request, '404_error.html')
    id = slug[0].prooduct_id
    if not id:
        return redirect('landingpage')
    else:
        product = Product.objects.get(id=id)
        sec_images = Secondary_images.objects.filter(product_id=product.id)
        all_products = Product.objects.all().order_by('-id')
        all_products = prepareProduct(all_products)
    product_category = ProductCategories.objects.all()
    context = {'product': product, 'sec_images': sec_images, 'profile':profile, 'product_category':product_category, 'all_products':all_products, 'user':user, 'slug':slug[0].product_slug}
    return render(request, 'preview.html', context)




def store(request):
    id = request.GET.get('id')
    user = str(request.user)
    profile = Profile.objects.filter(id=id)
    if not profile:
        return render(request, '404_error.html', {})
    products = Product.objects.filter(user=profile[0])   
    product_data = prepareProduct(products) 
    context = {'profile': profile[0], 'store_products': product_data, 'user':user}
    return render(request, 'store.html', context)







def search_query(request):
    query = request.GET.get('q', '')
    resp_list = getSearchFieldSuggestions(query)
    return JsonResponse(resp_list, safe=False)



def ai_image(request):
    process = productDetailLoader(request)
    if process["status"] == "success":
        return JsonResponse(process["data"])
    return render(request, 'ai_image.html')





def my_Cart(request):
    user = request.user
    if not user.is_authenticated:
        messages.error(request, 'Please login to add or buy product')
        return redirect('login')
    if request.GET.get('productId'):
        try:
            user_profile = Profile.objects.get(user=user)
            productId = request.GET.get('productId')
            slug = request.GET.get('slug')
            product = Product.objects.get(id=productId)
            if product.user == user_profile:
                messages.error(request, 'You can not add your own product to cart')
                return redirect('dashboard')    
            order = buyerCart(
                user=user_profile,
                product=product,
            )
            order.save()
            
            if request.GET.get('action') == 'buy':
                return redirect('myCart')
            messages.success(request, 'Product added to cart successfully')
            return redirect(f'/preview/{slug}')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('dashboard')
    elif request.GET.get('action') == 'delete':
        cart_id = request.GET.get('cart_id')
        cart = buyerCart.objects.get(id=cart_id)
        cart.delete()
        messages.success(request, 'Product removed from cart successfully')
        return redirect('myCart')
   
    user_profile = Profile.objects.get(user=user)
    cart = buyerCart.objects.filter(user=user_profile)
    context = {'cart':cart}
    return render(request, 'placeorder.html', context)
    




def buyer_Order(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to place order')
        return redirect('login')
    if request.method == 'POST':
        if request.GET.get('action') == 'place_order':
            data = json.loads(request.body)
            user = request.user
            user_profile = Profile.objects.get(user=user)
            order_details = data.get('order_details', [])
            order = buyerOrder(
            user=user_profile,
            )
            order.save()
            for item in order_details:
                product_id = item.get('product_id')
                product = Product.objects.get(id=product_id)
                product_id = item.get('product_id')
                productss = Product.objects.get(id=product_id)
                quantity = item.get('quantity')
                totalAmt = int(product.price) * int(quantity)
                buyer_product = buyerProducts(
                    order=order,
                    product=productss,
                    quantity=quantity,
                    totalAmount=totalAmt
                )
                buyer_product.save()
                # remove productsfrom cart
                cartProduct = buyerCart.objects.filter(product=productss)
                for cartProduct in cartProduct:
                    cartProduct.delete()
            return JsonResponse('Order placed successfully', safe=False)
        elif request.GET.get('action') == 'update_order':
            order_id = request.GET.get('order_id')
            orderStatus = request.POST.get('orderStatus')
            order = buyerOrder.objects.get(id=order_id)
            order.orderStatus = orderStatus
            order.save()
            return redirect('customerOrders')
    return JsonResponse('Invalid request', safe=False)
            


        








def customerOrders(request):
    user = request.user
    if not user.is_authenticated:
        messages.error(request, 'Please login to view orders')
        return redirect('login')
    
    user_profile = Profile.objects.get(user=request.user)

    if request.GET.get('action') == 'getproduct':
        order_id = request.GET.get('order_id')
        seller = Profile.objects.get(user=user)
        buyerorder = buyerOrder.objects.get(id=order_id)
        products = buyerProducts.objects.filter(order=buyerorder)
        allproducts = []
        for product in products:
            if product.product.user == seller:
                allproducts.append(product)
        grand_total = sum(int(product.totalAmount) for product in allproducts)
        
        context = {'products': allproducts, 'user_profile': user_profile, 'buyer':buyerorder, 'grand_total': grand_total}
        return render(request, 'customerOrder.html', context)
    elif request.GET.get('action') == 'delete':
        productid = request.GET.get('productId')
        product = buyerProducts.objects.get(id=productid)
        product.delete()
        messages.success(request, 'Product removed from order')
        return redirect(f'/customerOrders/?action=getproduct&order_id={product.order.id}')
    user_profile = Profile.objects.get(user=user)
    products = buyerProducts.objects.filter(product__user=user_profile).order_by('-id')
    orders = []
    if user_profile.user_type == 'seller':
        for product in products:
            orders.extend(buyerOrder.objects.filter(id=product.order.id).order_by('-id'))
    elif user_profile.user_type == 'buyer':
        products = buyerProducts.objects.filter(order__user=user_profile).order_by('-id')
        myOrders = buyerOrder.objects.filter(user=user_profile)
        
        context = {'bproducts': products, 'myOrders':myOrders, 'user_profile': user_profile}
        return render(request, 'customerOrder.html', context)
    context = {'orders': list(set(orders)), 'user_profile': user_profile}
    return render(request, 'customerOrder.html', context)