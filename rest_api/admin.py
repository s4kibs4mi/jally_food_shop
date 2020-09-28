from django.contrib import admin

from .models import Address, User, FoodCategory, FoodItem, Order, OrderItem, OrderLog

# Register your models here.
admin.site.register(Address)
admin.site.register(User)
admin.site.register(FoodCategory)
admin.site.register(FoodItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderLog)
