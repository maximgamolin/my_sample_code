from decimal import Decimal

from django.conf import settings

from store.models import Product


class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity_to_buy=1):
        product_id = str(product.get('id'))
        product_quantity = product.get('quantity')
        product_price = product.get('price')
        try:
            if quantity_to_buy > product_quantity - self.cart[product_id]['quantity']:
                return False
            self.cart[product_id]['quantity'] += quantity_to_buy
        except KeyError:
            if quantity_to_buy > product_quantity:
                return False
            self.cart[product_id] = {'quantity': quantity_to_buy,
                                     'price': product_price}
        self.save()
        return self.cart

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item.get('price'))
            item['total_price'] = item.get('price') * item.get('quantity')
            yield item

    def __len__(self):
        return sum(item.get('quantity') for item in self.cart.values())

    def get_product_total_price(self, product):
        product_price = self.cart[str(product.id)].get('price')
        product_quantity = self.cart[str(product.id)].get('quantity')
        return Decimal(product_price * product_quantity)

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
