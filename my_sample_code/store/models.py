from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Product name')
    vendor_code = models.CharField(max_length=10, unique=True, verbose_name='product_code')
    about_product = models.CharField(max_length=500, blank=True, default='', verbose_name='Info about product')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Product price')
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Product cost price')
    quantity = models.PositiveIntegerField(verbose_name='Qantity of product', default=0)

    def __str__(self):
        return f'ID {self.id}: {self.name}'


class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return f'Order {self.id}'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.id}'
