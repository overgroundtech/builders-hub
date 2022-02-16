from django.contrib import admin
from .models import Category, Product, ProductImage, Order, OrderItem

admin.site.site_header = "Builders Hub Admin"
admin.site.site_title = "Builders Hub Admin Portal"
admin.site.index_title = "Welcome to Builders Hub Admin Portal"


class ProductImageAdmin(admin.TabularInline):
    model = ProductImage
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'in_stock')
    list_filter = ('category', )
    inlines = [ProductImageAdmin]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'quantity', 'unit_price', 'total_price')
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('made_on', 'customer', 'status', 'paid', 'payment')
    ordering = ('made_on', 'paid',)
    inlines = [OrderItemAdmin]
