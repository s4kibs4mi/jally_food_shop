from rest_framework import serializers
from .models import Address
from .models import User
from .models import FoodCategory
from .models import FoodItem
from .models import Order
from .models import OrderItem
from .models import OrderLog


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'street', 'city', 'state', 'country', 'postcode')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'status', 'user_type', 'created_at')


class FoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ('id', 'name')


class FoodItemSerializer(serializers.ModelSerializer):
    food_category = FoodCategorySerializer()

    class Meta:
        model = FoodItem
        fields = ('id', 'name', 'food_picture', 'price', 'quantity', 'food_category', 'created_at', 'updated_at')


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('food_item', 'quantity', 'price', 'total')


class OrderLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLog
        fields = ('event', 'created_at')


class OrderSerializer(serializers.ModelSerializer):
    delivery_address = AddressSerializer()

    class Meta:
        model = Order
        fields = (
            'status', 'grand_total',
            'delivery_address', 'created_at', 'updated_at')
