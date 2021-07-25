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
        product_quantity, product_price = map(product.get, ('quantity', 'price'))
        if product_quantity >= quantity_to_buy > 0:
            if product_id not in self.cart:
                self.cart[product_id] = {'quantity': quantity_to_buy,
                                         'price': product_price}
            else:
                if product_quantity - self.cart[product_id]['quantity'] >= quantity_to_buy:
                    self.cart[product_id]['quantity'] += quantity_to_buy
                return False
            self.save()
            return self.cart
        return False

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
        product_price, product_quantity = map(self.cart[str(product.id)].get, ('price', 'quantity'))
        return Decimal(product_price * product_quantity)

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
