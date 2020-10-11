from django.forms import ModelForm
from rest_api.models import FoodItem
from rest_api.models import FoodCategory
from rest_api.models import Order


class FoodItemForm(ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'description', 'is_published', 'food_picture', 'food_category', 'price', 'quantity']
        exclude = ['created_at', 'updated_at']


class FoodCategoryForm(ModelForm):
    class Meta:
        model = FoodCategory
        fields = ['name']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        exclude = ['created_at', 'updated_at', 'user', 'sub_total', 'grand_total', 'payment_processing_fee',
                   'billing_address', 'delivery_address']
