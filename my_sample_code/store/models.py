from django.db import models, transaction


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

    def remove_items_from_stock(self, product, quantity_to_remove):
        """
        Remove requested quantity of product from stock when order created
        """
        if product.quantity >= quantity_to_remove:
            product.quantity -= quantity_to_remove
            product.save()
            return True
        return False

    def return_items_to_stock(self, product, quantity_to_return):
        """
        Return products to stock when order has been returned
        """
        product.quantity += quantity_to_return
        product.save()

    @transaction.atomic
    def add_products_from_cart_to_order(self, cart, order):
        """
        Add products from cart to order when we can sell requested quantity
        """
        selled_products = {}
        not_selled_products = {}
        order_products_to_create = []
        for item in cart:
            product_to_add, quantity_to_add = map(item.get, ('product', 'quantity'))
            total_price_to_add = cart.get_product_total_price(product_to_add)
            enough_quantiy_of_product = self.remove_items_from_stock(product_to_add, quantity_to_add)
            if enough_quantiy_of_product:
                order_products_to_create.append(OrderProduct(order=order,
                                                             product=product_to_add,
                                                             quantity=quantity_to_add,
                                                             ))
                selled_products[product_to_add.id] = {'quantity': quantity_to_add,
                                                      'total_price': total_price_to_add}
            else:
                not_selled_products[product_to_add.id] = int(product_to_add.quantity)
        OrderProduct.objects.bulk_create(order_products_to_create)
        return selled_products, not_selled_products

    def can_be_ordered(self, selled_products, not_selled_products):
        """
        Check order is not empty
        """
        if len(not_selled_products) > 0 and len(selled_products) == 0:
            return True
        return False

    @transaction.atomic
    def cancel_order(self, request):
        """
        Cancel sellected order
        """
        order_id = request.data.get('order_id')
        order_products = OrderProduct.objects.filter(order=order_id).all()
        order = Order.objects.get(id=order_id)
        for item in order_products:
            self.return_items_to_stock(item.product, item.quantity)
        order.returned = True
        order.save()


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.id}'
