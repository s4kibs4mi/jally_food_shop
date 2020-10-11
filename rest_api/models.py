from django.db import models
from jally_food_shop import settings


# Create your models here.

class Address(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    postcode = models.CharField(max_length=20)


class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    user_type = models.CharField(max_length=20)
    created_at = models.DateField()

    def __str__(self):
        return self.name


class FoodCategory(models.Model):
    name = models.CharField(max_length=50)


class FoodItem(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=10000, default='')
    food_picture = models.FileField(upload_to='documents/')
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    is_published = models.BooleanField(default=False)
    food_category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    sub_total = models.PositiveIntegerField()
    payment_processing_fee = models.PositiveIntegerField()
    grand_total = models.PositiveIntegerField()
    billing_address = models.ForeignKey(Address, related_name='order_billing_address', on_delete=models.CASCADE)
    delivery_address = models.ForeignKey(Address, related_name='order_delivery_address', on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    total = models.PositiveIntegerField()


class OrderLog(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    event = models.CharField(max_length=20)
    created_at = models.DateTimeField()
