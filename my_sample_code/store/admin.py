from django.contrib import admin
from django.contrib.admin import ModelAdmin

from store.models import Product, OrderProduct, Order


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    pass


@admin.register(OrderProduct)
class OrderProductAdmin(ModelAdmin):
    pass
