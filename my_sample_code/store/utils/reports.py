import datetime

from django.db.models import Sum, F
from django.utils.timezone import make_aware

from store.models import Order, OrderProduct


class Report:
    """
    Expects a date in the format 'dd.mm.YYYY'
    """

    def __init__(self, date_from, date_to):
        self.date_from = make_aware(datetime.datetime.strptime(date_from, "%d.%m.%Y"))
        self.date_to = make_aware(datetime.datetime.strptime(date_to, "%d.%m.%Y"))

    def get_proceeds(self):

        proceeds = Order.objects.values('total_price').filter(updated__range=(self.date_from, self.date_to),
                                                              returned=False).aggregate(proceed=Sum('total_price'))

        if proceeds.get('proceed'):
            return proceeds.get('proceed')

        return 0

    def get_profit(self):

        total_price = self.get_proceeds()

        cost_price = OrderProduct.objects.values('product__cost_price',
                                                 'quantity', ).filter(order__updated__range=(self.date_from,
                                                                                             self.date_to),
                                                                      order__returned=False).aggregate(
            profit=Sum(F('product__cost_price') * F('quantity')))

        if total_price and cost_price.get('profit'):
            profit = total_price - cost_price.get('profit')
            return profit
        return 0

    def get_selled_products(self):

        total_selled_products = Order.objects.values('total_products').filter(updated__range=(self.date_from,
                                                                                              self.date_to),
                                                                              returned=False).aggregate(
            total_selled_products=Sum('total_products'))

        if total_selled_products.get('total_selled_products'):
            return total_selled_products.get('total_selled_products')

        return 0

    def get_refund_orders(self):

        refund_orders = Order.objects.values('id').filter(updated__range=(self.date_from, self.date_to),
                                                          returned=True).count()

        return refund_orders
