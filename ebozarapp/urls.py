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
    path('ebazaar_support/', views.ebazaar_support, name='ebazaar_support'),
    
    ]
