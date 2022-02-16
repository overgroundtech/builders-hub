from django.contrib import admin
from .models import Category, Product, ProductImage, Order, OrderItem

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(Order)
admin.site.register(OrderItem)
