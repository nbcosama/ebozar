from django.contrib import admin
from .models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'store_name', 'user_type', 'verify')
    search_fields = ('user__username', 'store_name', 'user_type')
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_category', 'get_store_name')
    search_fields = ('product_name', 'product_category__category_name', 'user__store_name')

    def get_store_name(self, obj):
        return obj.user.store_name if obj.user else None
    get_store_name.admin_order_field = 'user__store_name'
    get_store_name.short_description = 'Store Name'
admin.site.register(OTP)
admin.site.register(Slug)
admin.site.register(Secondary_images)
@admin.register(Searched_Query)
class SearchedQueryAdmin(admin.ModelAdmin):
    list_display = ('query', 'date_time')
    search_fields = ('query', )
admin.site.register(ProductCategories)
admin.site.register(buyerCart)
admin.site.register(buyerOrder)
admin.site.register(buyerProducts)
admin.site.register(SubscribeUs)
@admin.register(VerifiedProfile)
class VerifiedProfileAdmin(admin.ModelAdmin):
    list_display = ('profile__store_name', 'is_verified')
    search_fields = ('profile__store_name', 'is_verified')
