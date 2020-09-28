from django.forms import ModelForm
from rest_api.models import FoodItem
from rest_api.models import FoodCategory


class FoodItemForm(ModelForm):
    class Meta:
        model = FoodItem
        fields = ['name', 'description', 'is_published', 'food_picture', 'food_category', 'price', 'quantity']
        exclude = ['created_at', 'updated_at']


class FoodCategoryForm(ModelForm):
    class Meta:
        model = FoodCategory
        fields = ['name']
