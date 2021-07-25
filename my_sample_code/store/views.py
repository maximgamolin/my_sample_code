from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from store.models import Product, Order
from store.serializers import (ProductSerializer,
                               ProductEconomicDataSerializer,
                               OrderSerializer
                               )
from store.utils.cart import Cart
from store.utils.reports import Report


class ProductAPIViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['name', 'price', 'cost_price']
    search_fields = ['name', 'price', 'cost_price']
    ordering_fields = ['name', 'price', 'cost_price']


class UpdateProductEconomicDataAPIView(generics.UpdateAPIView):
    serializer_class = ProductEconomicDataSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        product_id = self.request.data.get('id')
        product = get_object_or_404(Product, id=product_id)
        product.quantity = self.request.data.get('quantity')
        product.price = self.request.data.get('price')
        product.cost_price = self.request.data.get('cost_price')
        serializer.is_valid(raise_exception=True)
        product.save()
        return Response(self.request.data)


class CartAPIView(generics.GenericAPIView):

    def post(self, request):
        cart = Cart(request)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity_to_buy')
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductSerializer(product)
        added_product = cart.add(product=serializer.data, quantity_to_buy=quantity)
        if added_product:
            return Response({'detail': 'Product added to your cart', 'products': added_product})
        return Response({'detail': 'The quantity of the product is too large'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        Cart(request)
        cart = request.session.get('cart')
        return Response(cart, status=status.HTTP_200_OK)

    def delete(self, request):
        cart = Cart(request)
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        return Response({'detail': 'Item remover from cart'}, status=status.HTTP_204_NO_CONTENT)


class OrderAPIView(generics.GenericAPIView):
    serializer_class = OrderSerializer

    def get(self, request):
        order_id = request.session.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        serializer = OrderSerializer(order)
        return Response({"order": serializer.data})

    def post(self, request):
        cart = Cart(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        selled_products, not_selled_products = Order().add_products_from_cart_to_order(cart, order)
        if Order().can_be_ordered(selled_products, not_selled_products):
            return Response({'detail': 'Cant sell this quantity of selected products. Please change it',
                             'not_selled_products': not_selled_products},
                            status=status.HTTP_400_BAD_REQUEST)

        order = serializer.save()
        order_data = OrderSerializer(order).data
        request.session['order_id'] = order.id
        cart.clear()
        return Response({'detail': 'Order created',
                         'order_data': order_data,
                         'selled_products': selled_products,
                         'not_selled_products': not_selled_products},
                        status=status.HTTP_201_CREATED)

    def patch(self, request):
        try:
            Order().cancel_order(request)
        except ObjectDoesNotExist:
            return Response({'detail': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'detail': 'Order has been returned'}, status=status.HTTP_204_NO_CONTENT)


class ReportAPIView(generics.GenericAPIView):

    def get(self, request):
        date_from = request.data.get('date_from')
        date_to = request.data.get('date_to')
        try:
            products_report = Report(date_from, date_to).get_report_products()
        except (ValueError, TypeError):
            return Response({'detail': "No date range was specified"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"products": products_report})
