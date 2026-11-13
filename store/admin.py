from django.contrib import admin
from .models import Product, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'price_at_purchase', 'quantity', 'subtotal')
    can_delete = False


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity', 'is_in_stock', 'created_at')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    list_editable = ('price', 'quantity')
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'category', 'description', 'image')
        }),
        ('Inventory & Pricing', {
            'fields': ('price', 'quantity')
        }),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'phone', 'payment_method', 'payment_status', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_method', 'payment_status', 'created_at')
    search_fields = ('user__username', 'full_name', 'phone', 'shipping_address')
    list_editable = ('status', 'payment_status')
    readonly_fields = ('created_at', 'updated_at', 'total_amount')
    inlines = [OrderItemInline]

