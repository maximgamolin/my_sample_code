from django.db import transaction

from store.models import OrderProduct

from store.serializers import OrderSerializer


def remove_products_because_order(product, quantity_to_remove):
    if product.quantity >= quantity_to_remove:
        product.quantity -= quantity_to_remove
        product.save()
        return True
    return False


def return_products_because_reset_order(product, quantity_to_add):
    product.quantity += quantity_to_add
    product.save()
    return True


@transaction.atomic
def add_products_to_order(cart, order):
    selled_products = {}
    not_selled_products = {}
    order_products_to_create = []
    for item in cart:
        product_to_add, quantity_to_add = map(item.get, ('product', 'quantity'))
        total_price_to_add = cart.get_product_total_price(product_to_add)
        if remove_products_because_order(product_to_add, quantity_to_add):
            order_products_to_create.append(OrderProduct(order=order,
                                                         product=product_to_add,
                                                         quantity=quantity_to_add,
                                                         ))
            selled_products[product_to_add.id] = {'quantity': quantity_to_add,
                                                  'total_price': total_price_to_add}
        else:
            # dict{'product_id': max_quantity_than_user_can_buy_now}
            not_selled_products[product_to_add.id] = int(product_to_add.quantity)
    OrderProduct.objects.bulk_create(order_products_to_create)
    cart.clear()
    order_data = OrderSerializer(order).data
    return order_data, selled_products, not_selled_products
