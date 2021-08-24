import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import RequestFactory
from store.views import OrderAPIView
from django.contrib.sessions.middleware import SessionMiddleware

from store.models import Product, OrderProduct
from store.serializers import ProductSerializer
from store.tests.utils.factories import ProductFactory, CartFactory
from django.conf import settings


class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.product1 = Product.objects.create(name='test_product_1',
                                               about_product='about_test_product_1',
                                               vendor_code='A1',
                                               price=100,
                                               cost_price=10,
                                               quantity=1,
                                               )

        self.product2 = Product.objects.create(name='test_product_2',
                                               about_product='about_test_product_2',
                                               vendor_code='A2',
                                               price=200,
                                               cost_price=30,
                                               quantity=2)

        self.product3 = Product.objects.create(name='the_product_than_search_will_not_find_3',
                                               about_product='about_test_product_3',
                                               vendor_code='A3',
                                               price=300,
                                               cost_price=30,
                                               quantity=3)

    def test_get_product_list(self):
        url = reverse('product-list')
        response = self.client.get(url)
        serialized_data = ProductSerializer([self.product1, self.product2, self.product3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serialized_data, response.data)

    def test_get_product_list_filter(self):
        url = reverse('product-list')
        response = self.client.get(url, data={'cost_price': 30})
        serialized_data = ProductSerializer([self.product2, self.product3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serialized_data, response.data)

    def test_get_product_list_search(self):
        url = reverse('product-list')
        response = self.client.get(url, data={'search': 'test_product'})
        serialized_data = ProductSerializer([self.product1, self.product2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serialized_data, response.data)

    def test_get_product_list_inverse_order(self):
        url = reverse('product-list')
        response = self.client.get(url, data={'ordering': '-name'})
        serialized_data = ProductSerializer([self.product3, self.product2, self.product1], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serialized_data, response.data)

    def test_post_create(self):
        self.assertEqual(3, Product.objects.all().count())
        url = reverse('product-list')
        data = {"name": "test_product_4",
                "vendor_code": "A4",
                "price": 400,
                "cost_price": 100,
                "quantity": 40
                }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Product.objects.all().count())

    def test_post_create_not_unique_vendor_code(self):
        self.assertEqual(3, Product.objects.all().count())
        url = reverse('product-list')
        data = {"name": "test_product_4",
                "vendor_code": "A1",
                "price": 400,
                "cost_price": 100,
                "quantity": 40
                }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        error_message = 'product with this product_code already exists.'
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(response.data['vendor_code'][0], error_message)
        self.assertEqual(3, Product.objects.all().count())

    def test_put_update(self):
        url = reverse('product-detail', args=(self.product1.id,))
        data = {"name": "test_product_1",
                'vendor_code': 'A1',
                "price": 10000,
                "cost_price": 5000,
                "quantity": 500
                }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.product1.refresh_from_db()
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(10000, self.product1.price)
        self.assertEqual(5000, self.product1.cost_price)
        self.assertEqual(500, self.product1.quantity)

    def test_delete(self):
        url = reverse('product-detail', args=(self.product1.id,))
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        url = reverse('product-list')
        response = self.client.get(url)
        serialized_data = ProductSerializer([self.product2, self.product3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serialized_data, response.data)

    def test_get_one_product(self):
        url = reverse('product-detail', args=(self.product3.id,))
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        serialized_data = ProductSerializer(self.product3).data
        self.assertEqual(serialized_data, response.data)


class UpdateProductEconomicDataAPIViewTestCase(APITestCase):

    def setUp(self):
        self.product1 = Product.objects.create(name='test_product_1',
                                               about_product='about_test_product_1',
                                               price=100,
                                               cost_price=10,
                                               quantity=1,
                                               )

    def request(self, data):
        response = self.client.put(reverse('update_product_economic_data'), data=data, format='json')
        return response.status_code, json.loads(response.content)

    def test_change_quantity(self):
        status_code, content = self.request({
            'id': self.product1.id,
            'price': self.product1.price,
            'cost_price': self.product1.cost_price,
            'quantity': 100,
        })
        self.product1.refresh_from_db()
        self.assertEqual(content['quantity'], self.product1.quantity)
        self.assertEqual(status_code, 200)

    def test_change_cost__price(self):
        status_code, content = self.request({
            'id': self.product1.id,
            'price': self.product1.price,
            'cost_price': 80,
            'quantity': self.product1.quantity,
        })

        self.product1.refresh_from_db()
        self.assertEqual(content['cost_price'], self.product1.cost_price)
        self.assertEqual(status_code, 200)

    def test_change_price(self):
        status_code, content = self.request({
            'id': self.product1.id,
            'price': 500,
            'cost_price': self.product1.cost_price,
            'quantity': self.product1.quantity,
        })
        self.product1.refresh_from_db()
        self.assertEqual(content['price'], self.product1.price)
        self.assertEqual(status_code, 200)

    def test_negative_not_found_product(self):
        status_code, content = self.request({
            'id': 0,
            'price': 500,
            'cost_price': 50,
            'quantity': 30,
        })
        self.product1.refresh_from_db()
        error_text = "Not found."
        self.assertEqual(content['detail'], error_text)
        self.assertEqual(status_code, 404)


class CartAPIViewTestCase(APITestCase):

    def setUp(self):
        self.product1 = Product.objects.create(name='test_product_1',
                                               about_product='about_test_product_1',
                                               vendor_code='A1',
                                               price=100,
                                               cost_price=10,
                                               quantity=100,
                                               )

        self.product2 = Product.objects.create(name='test_product_2',
                                               about_product='about_test_product_2',
                                               vendor_code='A2',
                                               price=200,
                                               cost_price=30,
                                               quantity=200)

    def test_get_empty_cart(self):
        response = self.client.get(reverse('cart'), format='json')
        status_code, content = response.status_code, json.loads(response.content)
        self.assertEqual(content, {})
        self.assertEqual(status_code, 200)

    def test_post_add_product_to_cart(self):
        data = {"product_id": self.product1.id,
                "quantity_to_buy": 10}
        response = self.client.post(reverse('cart'), data=data, format='json')
        status_code, content = response.status_code, json.loads(response.content)
        added_product_data = {str(data["product_id"]): {
            "quantity": data["quantity_to_buy"], "price": str(self.product1.price) + ".00"}
        }
        self.assertEqual(content["detail"], "Product added to your cart")
        self.assertEqual(content["products"], added_product_data)
        self.assertEqual(status_code, 200)

    def test_post_and_get_add_second_product_to_cart(self):
        data_product1 = {"product_id": self.product1.id,
                         "quantity_to_buy": 10}
        response = self.client.post(reverse('cart'), data=data_product1, format='json')
        status_code, content = response.status_code, json.loads(response.content)
        added_product1_data = {str(data_product1["product_id"]): {"quantity": data_product1["quantity_to_buy"],
                                                                  "price": str(self.product1.price) + ".00"}}
        self.assertEqual(content["detail"], "Product added to your cart")
        self.assertEqual(content["products"], added_product1_data)
        self.assertEqual(status_code, 200)

        data_product2 = {"product_id": self.product2.id,
                         "quantity_to_buy": 5}
        response = self.client.post(reverse('cart'), data=data_product2, format='json')
        status_code, content = response.status_code, json.loads(response.content)

        added_two_products_data = {str(data_product1["product_id"]): {"quantity": data_product1["quantity_to_buy"],
                                                                      "price": str(self.product1.price) + ".00"},
                                   str(data_product2["product_id"]): {"quantity": data_product2["quantity_to_buy"],
                                                                      "price": str(self.product2.price) + ".00"}
                                   }
        self.assertEqual(content["detail"], "Product added to your cart")
        self.assertEqual(content["products"], added_two_products_data)
        self.assertEqual(status_code, 200)

        response = self.client.get(reverse('cart'), format='json')
        status_code, content = response.status_code, json.loads(response.content)
        self.assertEqual(content, added_two_products_data)
        self.assertEqual(status_code, 200)

    def test_post_update_quantity_of_product_in_the_cart(self):
        data1 = {"product_id": self.product1.id,
                 "quantity_to_buy": 10}
        response = self.client.post(reverse('cart'), data=data1, format='json')
        status_code, content = response.status_code, json.loads(response.content)
        added_product_data1 = {str(data1["product_id"]): {
            "quantity": data1["quantity_to_buy"],
            "price": str(self.product1.price) + ".00"}
        }

        self.assertEqual(content["detail"], "Product added to your cart")
        self.assertEqual(content["products"][str(self.product1.id)]["quantity"], data1["quantity_to_buy"])
        self.assertEqual(content["products"], added_product_data1)
        self.assertEqual(status_code, 200)

        data2 = {"product_id": self.product1.id,
                 "quantity_to_buy": 5}
        response = self.client.post(reverse('cart'), data=data2, format='json')
        status_code, content = response.status_code, json.loads(response.content)
        added_product_data2 = {str(data1["product_id"]): {
            "quantity": data1["quantity_to_buy"] + data2["quantity_to_buy"],
            "price": str(self.product1.price) + ".00"}
        }

        self.assertEqual(content["detail"], "Product added to your cart")
        self.assertEqual(content["products"][str(self.product1.id)]["quantity"],
                         data1["quantity_to_buy"] + data2["quantity_to_buy"])
        self.assertEqual(content["products"], added_product_data2)
        self.assertEqual(status_code, 200)

    def test_post_negative_add_product_to_cart_quantity_is_too_large(self):
        data = {"product_id": self.product1.id,
                "quantity_to_buy": 10000000}
        response = self.client.post(reverse('cart'), data=data, format='json')
        status_code, content = response.status_code, json.loads(response.content)
        self.assertEqual(content["detail"], 'The quantity of the product is too large')
        self.assertEqual(status_code, 400)

    def test_post_negative_add_product_to_cart_invalid_product_id(self):
        data = {"product_id": 0,
                "quantity_to_buy": 10000000}
        response = self.client.post(reverse('cart'), data=data, format='json')
        status_code, content = response.status_code, json.loads(response.content)
        self.assertEqual(content["detail"], 'Not found.')
        self.assertEqual(status_code, 404)


class OrderAPIViewTestCase(APITestCase):

    def setUp(self):
        self.start_product_1_quantity = 100
        self.start_product_2_quantity = 200

        self.product1 = ProductFactory().make_item({"quantity": self.start_product_1_quantity})
        self.product2 = ProductFactory().make_item({"quantity": self.start_product_2_quantity})

        self.quantity_to_buy_1 = 10
        self.quantity_to_buy_2 = 5

        self.request_factory = RequestFactory()
        self.cart_factory = CartFactory()
        self.cart_factory.add_to_cart(self.product1.id, self.quantity_to_buy_1, self.product1.price)
        self.cart_factory.add_to_cart(self.product2.id, self.quantity_to_buy_2, self.product2.price)


    def test_get_empty_order(self):
        response = self.client.get(reverse('order'), format='json')
        status_code, content = response.status_code, json.loads(response.content)
        self.assertEqual(content["detail"], "Not found.")
        self.assertEqual(status_code, 404)

    def test_post_create_order_all_products_selled(self):
        self.assertEqual(OrderProduct.objects.count(), 0)
        data = {"customer_name": "test_name",
                "email": "test@email.com",
                "address": "test street",
                "postal_code": 123456,
                "city": "test_city"}

        request = self.request_factory.post(reverse('order'), data=data, content_type='application/json')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session[settings.CART_SESSION_ID] = self.cart_factory.cart
        request.session.save()
        response = OrderAPIView.as_view()(request)
        response.render()
        status_code, content = response.status_code, json.loads(response.content)

        expected_order_data = {'id': content['order_data']['id'],
                               'customer_name': 'test_name',
                               'email': 'test@email.com',
                               'address': 'test street',
                               'postal_code': '123456',
                               'city': 'test_city',
                               'created': content['order_data']['created'],
                               'updated': content['order_data']['updated'],
                               'returned': False}
        expected_selled_products = {str(self.product1.id): {"quantity": self.quantity_to_buy_1,
                                                            "total_price":
                                                                float(self.product1.price * self.quantity_to_buy_1)},
                                    str(self.product2.id): {"quantity": self.quantity_to_buy_2,
                                                            "total_price":
                                                                float(self.product2.price * self.quantity_to_buy_2)}
                                    }
        expected_not_selled_products = {}
        self.assertEqual(content["detail"], "Order created")
        self.assertEqual(content["order_data"], expected_order_data)
        self.assertEqual(content["selled_products"], expected_selled_products)
        self.assertEqual(content["not_selled_products"], expected_not_selled_products)
        self.assertEqual(status_code, 201)

        self.product1.refresh_from_db()
        self.product2.refresh_from_db()
        self.assertEqual(self.product1.quantity, self.start_product_1_quantity-self.quantity_to_buy_1)
        self.assertEqual(self.product2.quantity, self.start_product_2_quantity-self.quantity_to_buy_2)

        self.assertEqual(OrderProduct.objects.count(), 2)
        for product, quantity in [(self.product1, self.quantity_to_buy_1),
                                  (self.product2, self.quantity_to_buy_2)]:
            with self.subTest():
                order_product = OrderProduct.objects\
                    .filter(product=product, order_id=content['order_data']['id']).first()
                self.assertIsNotNone(order_product)
                self.assertEqual(order_product.quantity, quantity)
