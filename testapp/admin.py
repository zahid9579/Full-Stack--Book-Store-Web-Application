from django.contrib import admin
from .models import Book, Cart, CartItem, Category, DeliveryInfo
# Register your models here.

admin.site.register(Book)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Category)
admin.site.register(DeliveryInfo)