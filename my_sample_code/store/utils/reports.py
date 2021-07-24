import datetime
from psycopg2.extras import Json

from django.db.models import Sum, F, Case, When, Count
from django.utils.timezone import make_aware

from store.models import Order, OrderProduct


class Report:
    """
    Expects a date in the format 'dd.mm.YYYY'
    """

    def __init__(self, date_from, date_to):
        self.date_from, self.date_to = map(self.reformat_date, (date_from, date_to))
        self.date_to += datetime.timedelta(days=1)

    def reformat_date(self, date):
        return make_aware(datetime.datetime.strptime(date, "%d.%m.%Y"))

    def get_report_products(self):
        products_sells = OrderProduct.objects.filter(
            order__updated__range=(self.date_from, self.date_to)).values('product__id').annotate(
            refund_products=Sum(Case(When(order__returned=True, then='quantity'))),
            quantity_selled_products=Sum(F('quantity')) - F('refund_products'),
            proceeds_selled_product=F('product__price') * F('quantity_selled_products'),
            profit=F('proceeds_selled_product') - (
                    F('product__cost_price') * F('quantity_selled_products')),
        )
        return products_sells
