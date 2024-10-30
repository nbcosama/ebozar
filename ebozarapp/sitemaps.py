# sitemaps.py
from django.contrib.sitemaps import Sitemap
from .models import Slug  # Replace with your actual Product model

class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        products = Slug.objects.all()
        data = []
        for product in products:
            data.append(f'/preview/{product.product_slug}')
        data+=[
            "/",
            "/login/",
            "/signup/",
            "/preview/",
            "/store/",
        ]
        return data

    def location(self, item):
        return item
