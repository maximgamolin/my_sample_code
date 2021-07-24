from django.test import TestCase

from store.models import Product
from store.serializers import ProductSerializer


class ProductSerializerTestCase(TestCase):
    def test_good_result(self):
        product1 = Product.objects.create(name='test_product_1',
                                          vendor_code='A1',
                                          about_product='about_test_product_1',
                                          price=100,
                                          cost_price=10,
                                          quantity=1,
                                          )
        product2 = Product.objects.create(name='test_product_2',
                                          vendor_code='A2',
                                          about_product='about_test_product_2',
                                          price=200,
                                          cost_price=20,
                                          quantity=2)
        serialized_data = ProductSerializer([product1, product2], many=True).data
        expected_data = [
            {
                'id': product1.id,
                'name': 'test_product_1',
                'vendor_code': 'A1',
                'about_product': 'about_test_product_1',
                'price': '100.00',
                'cost_price': '10.00',
                'quantity': 1
            },
            {
                'id': product2.id,
                'name': 'test_product_2',
                'vendor_code': 'A2',
                'about_product': 'about_test_product_2',
                'price': '200.00',
                'cost_price': '20.00',
                'quantity': 2
            }
        ]
        self.assertEqual(serialized_data, expected_data)
