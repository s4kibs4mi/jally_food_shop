from rest_framework import serializers
from .models import Address
from .models import User
from .models import FoodCategory
from .models import FoodItem
from .models import Order
from .models import OrderItem
from .models import OrderLog


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ('id', 'street', 'city', 'state', 'country', 'postcode')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'status', 'user_type', 'created_at')


class FoodCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ('id', 'name')


class FoodItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FoodItem
        fields = ('id', 'name', 'food_picture', 'price', 'quantity', 'food_category', 'created_at', 'updated_at')


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = (
            'user', 'status', 'sub_total', 'payment_processing_fee', 'grand_total', 'billing_address',
            'delivery_address', 'created_at', 'updated_at')


class OrderItemCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('food_item', 'quantity', 'price', 'total')


class OrderLogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderLog
        fields = ('event', 'created_at')
