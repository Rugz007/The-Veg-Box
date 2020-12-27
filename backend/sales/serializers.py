from rest_framework import serializers
from sales.models import Order, OrderItem

class AddOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'

class AddOrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'