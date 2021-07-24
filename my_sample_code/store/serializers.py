from rest_framework.serializers import ModelSerializer

from store.models import Product, Order


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductEconomicDataSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'quantity', 'price', 'cost_price')


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
