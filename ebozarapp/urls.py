from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from .sitemaps import ProductSitemap

sitemaps = {
    'products': ProductSitemap,
}

urlpatterns = [
    path('', views.landingpage, name='landingpage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('preview/<str:slug>', views.preview, name='preview'),
    path('store/', views.store, name='store'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('logout/', views.logout, name='logout'),
    path('add_product/', views.add_product, name='add_product'),
    path('profile/', views.profile, name='profile'),
    path('update_product/', views.update_product, name='update_product'),
    path('send_username/', views.send_username, name='send_username'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('search_query/', views.search_query, name='search'),
    path('ekhoji_support/', views.ekhoji_support, name='ekhoji_support'),
    path('become-a-seller/', views.became_a_seller, name='become-a-seller'),
    path('ai_image/', views.ai_image, name='ai_image'),
    path('myCart/', views.my_Cart, name='myCart'),
    path('buyerOrder/', views.buyer_Order, name='buyerOrder'),
    path('getDirection/', views.getDirection, name='getDirection'),
    path('customerOrders/', views.customerOrders, name='customerOrders'),
    path('terms-condition', views.termscondition, name='terms-condition'),
    path('privacy', views.privacy_policy, name='privacy'),
    path('faqs', views.faqs, name='faqs'),
    path('ourstory', views.ourstory, name='ourstory'),
    path('career', views.career, name='career'),
    path('subscribeus', views.subscribeus, name='subscribeus'),
    path('allstores/', views.allstores, name='allstores'),
    ]
