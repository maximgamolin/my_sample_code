from store.models import OrderProduct


class AddProductsToOrdersFromCart:

    def __init__(self, cart, order):
        self._cart = cart
        self._order = order
        self.selled_products = {}
        self.not_selled_products = {}
        self._product_for_creation = []

    @staticmethod
    def _remove_items_from_stock(product, quantity_to_remove):
        """
        Remove requested quantity of product from stock when order created
        """
        if product.quantity >= quantity_to_remove:
            product.quantity -= quantity_to_remove
            product.save()
            return True
        return False

    def _init_order_product_or_add_unsaleable_postion(self, product, quantity):
        if not self._remove_items_from_stock(product, quantity):
            self.not_selled_products[product.id] = int(product.quantity)
            return
        self.selled_products[product.id] = {
            'quantity': quantity,
            'total_price': self._cart.get_product_total_price(product)
        }
        self._product_for_creation.append(
            OrderProduct(
                order=self._order, product=product, quantity=quantity
            )
        )

    def transfer_positions(self):
        for position in self._cart:
            product = position.get('product')
            quantity = position.get('quantity')
            self._init_order_product_or_add_unsaleable_postion(
                product, quantity
            )

        OrderProduct.objects.bulk_create(self._product_for_creation)



