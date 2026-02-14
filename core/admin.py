from django.contrib import admin
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'discount_price', 'stock']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'payment_method', 'payment_status', 'order_status', 'created_at']
    list_filter = ['payment_method', 'payment_status', 'order_status']
    search_fields = ['user__username', 'transaction_id']
    actions = ['mark_payment_verified', 'confirm_order', 'mark_delivered']
    
    def mark_payment_verified(self, request, queryset):
        from django.utils import timezone
        queryset.update(payment_status=True, order_status='confirmed')
        for order in queryset:
            Payment.objects.filter(order=order).update(verified=True, verified_at=timezone.now())
    mark_payment_verified.short_description = "✅ Verify payment & confirm order"
    
    def confirm_order(self, request, queryset):
        queryset.update(order_status='confirmed')
    confirm_order.short_description = "📦 Confirm order"
    
    def mark_delivered(self, request, queryset):
        queryset.update(order_status='delivered')
    mark_delivered.short_description = "🚚 Mark as delivered"

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['order', 'transaction_id', 'method', 'amount', 'verified', 'created_at']
    list_filter = ['method', 'verified']