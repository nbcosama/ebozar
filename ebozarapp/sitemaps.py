# sitemaps.py
from django.contrib.sitemaps import Sitemap
from .models import Slug, Profile  # Replace with your actual Product model

class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        products = Slug.objects.all()
        stores = Profile.objects.all()
        
        data = []
        for product in products:
            data.append(f'/preview/{product.product_slug}')

        for store in stores:
            data.append(f'/store/?id={store.id}')
        data+=[
            "/",
            "/login/",
            "/signup/",
        ]
        return data

    def location(self, item):
        return item
