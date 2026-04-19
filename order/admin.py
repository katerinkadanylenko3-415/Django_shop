from django.contrib import admin

from .models import OrderItem, Order


class OrderItemInLine(admin.TabularInline):
    model = OrderItem


from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'first_name', 'status', 'created', 'paid']
    list_filter = ['status', 'created', 'paid']
    list_editable = ['status', 'paid']
    inlines = [OrderItemInLine]