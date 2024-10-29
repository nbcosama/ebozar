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



def landingpage(request):
    query = request.GET.get('q', '')
    products = Product.objects.all().order_by('-id')
    stores = Profile.objects.all()
    if query:
        products = products.filter(
            Q(product_name__icontains=query) |
            Q(brand__icontains=query) |
            Q(color__icontains=query) |
            Q(price__icontains=query) |
            Q(condtion__icontains=query) |
            Q(quantity__icontains=query) |
            Q(user__store_name__icontains=query)
        )
        stores = stores.filter(
            Q(store_name__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(address__icontains=query) |
            Q(country__icontains=query) |
            Q(city__icontains=query) |
            Q(user__username__icontains=query)
        )
    context = {'products': products, 'query': query, 'stores': stores}
    return render(request, 'landingpage.html', context)






def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
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
                messages.success(request, 'Log In successful')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('login')
    return render(request, 'login.html')







def logout(request):
    auth_logout(request)
    messages.success(request, 'Log Out successfully')
    return redirect('login')








def signup(request):
    if request.user.is_authenticated:
        messages.error(request, 'You are already logged in. please logout to create a new account')
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
            "user_type": user_type
        }
        user_data_json = json.dumps(user_data)
        username = store_name.replace(" ", "_").lower()
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use.')
            return redirect('signup')
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
                        email = emails
                    )
                profile.save()
                # Automatically log in the user after signing up
                auth_login(request, user)  
                messages.success(request, 'Account created successfully! Please update your profile')
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
        quantity = request.POST.get('quantity')
        product_image = request.FILES.get('image')
        if not product_name or not price or not condtion or not quantity or not product_image:
            messages.error(request, 'All fields are required')
            return redirect('add_product')
        if user_profile.verify == False:
            messages.error(request, 'Please verify your account to add product. To verify account contact support team')
            return redirect('dashboard')
        product = Product(
            user=user_profile, 
            product_name=product_name, 
            price=price,
            condtion=condtion, 
            product_image=product_image, 
            brand=brand, 
            color=color, 
            quantity=quantity
            )
        product.save()
        messages.success(request, 'Product added successfully')
        return redirect('add_product')
    user = request.user
    user_profile = Profile.objects.get(user=user)
    context = {'user_profile': user_profile}
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
        quantity = request.POST.get('quantity')
        product_image = request.FILES.get('image')
        product.product_name = product_name
        product.price = price
        product.condtion = condtion
        product.brand = brand
        product.color = color
        product.quantity = quantity
        if product_image:
            product.product_image = product_image
        product.save()
        messages.success(request, 'Product updated successfully')
        return redirect('dashboard')
    id = request.GET.get('product_id')
    user = request.user
    user_profile = Profile.objects.get(user=user)
    product = Product.objects.get(id=id)
    context = {'user_profile':user_profile, 'product': product}
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
            user_profile.phone_number = phone_number
            user_profile.address = address
            user_profile.bio = bio
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









def preview(request):
    id = request.GET.get('id')
    product = Product.objects.get(id=id)
    all_products = Product.objects.all().order_by('-id')
    context = {'product': product, 'all_products':all_products}
    return render(request, 'preview.html', context)









def store(request):
    id = request.GET.get('id')
    profile = Profile.objects.get(id=id)
    store_product = Product.objects.filter(user=profile)    
    context = {'profile': profile, 'store_products': store_product}
    return render(request, 'store.html', context)







