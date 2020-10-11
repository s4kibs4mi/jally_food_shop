from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.shortcuts import redirect
from rest_api.forms import FoodItemForm
from rest_api.forms import FoodCategoryForm
from rest_api.forms import OrderForm
from rest_api.models import FoodItem
from rest_api.models import FoodCategory
from rest_api.models import OrderItem
from rest_api.models import OrderLog
from rest_api.models import Order
from rest_api.models import User
from rest_api.models import Address
from rest_api.serializers import FoodItemSerializer
from rest_api.serializers import OrderSerializer
from rest_api.serializers import OrderItemSerializer
from rest_api.serializers import UserSerializer
from datetime import datetime
from rest_api import jwt
from django.db import transaction


# Create your views here.

@api_view(['GET'])
def overview(request):
    urls = {
        'Register': 'POST /users/',
        'Login': 'POST /login/',
        'Profile': 'GET /users/',
        'Create Order': 'POST /orders/',
        'Get Order': 'GET /orders/<str:pk>',
        'List Orders': 'GET /orders/',
    }
    return Response(urls)


@api_view(['POST'])
def users_register(request):
    try:
        user = User()
        user.name = request.data["name"]
        user.status = "active"
        user.password = request.data["password"]
        user.email = request.data["email"]
        user.created_at = datetime.now()

        try:
            user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "error": "email " + user.email + " already registered"
            }, status=status.HTTP_409_CONFLICT)
    except KeyError as e:
        print(e)

        msg = {
            'error': str(e) + " is required"
        }
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)

        msg = {
            'error': "Invalid request"
        }
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def users_login(request):
    try:
        email = request.data["email"]
        password = request.data["password"]

        users = User.objects.filter(email=email, password=password)
        if users.__len__() != 0:
            token = jwt.encode(users[0].id)
            return Response({'token': token}, status=status.HTTP_200_OK)

        return Response({}, status=status.HTTP_401_UNAUTHORIZED)
    except KeyError as e:
        print(e)

        msg = {
            'error': str(e) + " is required"
        }
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)

        msg = {
            'error': "Invalid request"
        }
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def users_profile(request):
    pass


@transaction.atomic()
@api_view(['POST'])
def orders_create(request):
    try:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)

        sp = transaction.savepoint()

        total_cost = 0
        items = request.data["items"]
        ordered_items = []

        for i in items:
            print(i)

            food_item = FoodItem.objects.get(id=i["id"])
            order_item = OrderItem()
            order_item.food_item = food_item
            order_item.price = food_item.price
            order_item.quantity = i["quantity"]
            order_item.total = order_item.price * order_item.quantity

            if food_item.quantity - order_item.quantity < 0:
                transaction.savepoint_rollback(sp)

                return Response({
                    'error': 'item: ' + food_item.name + ' is unavailable'
                }, status.HTTP_400_BAD_REQUEST)

            food_item.quantity = food_item.quantity - order_item.quantity
            food_item.save()

            total_cost += order_item.total
            ordered_items.append(order_item)

        delivery_address_params = request.data["delivery_address"]
        address = Address()
        address.street = delivery_address_params["street"]
        address.city = delivery_address_params["city"]
        address.state = delivery_address_params["state"]
        address.country = delivery_address_params["country"]
        address.postcode = delivery_address_params["postcode"]
        address.save()

        order = Order()
        order.user = user
        order.status = "pending"
        order.sub_total = total_cost
        order.payment_processing_fee = 0
        order.grand_total = total_cost
        order.billing_address = address
        order.delivery_address = address
        order.created_at = datetime.now()
        order.updated_at = datetime.now()
        order.save()

        for i in ordered_items:
            i.order = order
            i.save()

        resp = {
            "id": order.id
        }

        transaction.savepoint_commit(sp)

        return Response(resp, status=status.HTTP_201_CREATED)
    except KeyError as e:
        print(e)

        msg = {
            'error': str(e) + " is required"
        }
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)

        msg = {
            'error': "Invalid request"
        }
        return Response(msg, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def orders_get(request, id):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)

    order = Order.objects.filter(user=user, id=id).first()
    serializer = OrderSerializer(order)
    ordered_items = OrderItem.objects.filter(order=order)
    ordered_items_serializer = OrderItemSerializer(ordered_items, many=True)

    resp = serializer.data
    resp["items"] = ordered_items_serializer.data

    return Response(resp)


@api_view(['GET'])
def orders_list(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    orders = Order.objects.filter(user=user).order_by('-created_at')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def products_list(request):
    food_items = FoodItem.objects.all().order_by('-created_at')
    resp = Response(FoodItemSerializer(food_items, many=True).data)
    resp['Access-Control-Allow-Origin'] = '*'
    resp['Access-Control-Allow-Headers'] = '*'
    return resp


# Store endpoints start

def store_home(request):
    return redirect("/v1/store/products")


def store_add_product(request):
    form = FoodItemForm()

    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/v1/store/products")

    context = {'form': form}
    return render(request, 'store/add_product.html', context)


def store_list_products(request):
    food_items = FoodItem.objects.all().order_by('-created_at')
    ctx = {
        'food_items': food_items
    }
    return render(request, "store/index.html", ctx)


def store_update_product(request, id):
    instance = FoodItem.objects.get(id=id)
    form = FoodItemForm(None, instance=instance)

    if request.method == "POST":
        form = FoodItemForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("/v1/store/products")

    ctx = {
        'form': form
    }
    return render(request, 'store/update_product.html', ctx)


def store_delete_product(request, id):
    instance = FoodItem.objects.get(id=id)
    instance.delete()
    return redirect("/v1/store/products")


def store_add_food_category(request):
    form = FoodCategoryForm()

    if request.method == "POST":
        form = FoodCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/v1/store/categories")

    context = {
        'form': form,
        'msg': ''
    }
    return render(request, "store/add_category.html", context)


def store_list_categories(request):
    food_categories = FoodCategory.objects.all()
    ctx = {
        'food_categories': food_categories
    }
    return render(request, "store/list_categories.html", ctx)


def store_update_category(request, id):
    instance = FoodCategory.objects.get(id=id)
    form = FoodCategoryForm(None, instance=instance)

    if request.method == "POST":
        form = FoodCategoryForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("/v1/store/categories")

    ctx = {
        'form': form
    }
    return render(request, 'store/update_category.html', ctx)


def store_delete_category(request, id):
    instance = FoodCategory.objects.get(id=id)
    instance.delete()
    return redirect("/v1/store/categories")


def store_list_orders(request):
    orders = Order.objects.all().order_by('-created_at')

    formatted_orders = []

    for o in orders:
        u = User.objects.get(id=o.user_id)

        formatted_order = {
            'id': o.id,
            'at': o.created_at,
            'user_name': u.name,
            'total': o.grand_total,
            'status': o.status,
        }

        formatted_items = []
        ordered_items = OrderItem.objects.filter(order=o)
        for i in ordered_items:
            formatted_items.append({
                'name': i.food_item.name,
                'image': i.food_item.food_picture,
                'price': i.price,
                'quantity': i.quantity,
                'total': i.total,
            })

        formatted_order['items'] = formatted_items

        formatted_orders.append(formatted_order)

    ctx = {
        'orders': formatted_orders
    }
    return render(request, "store/orders.html", ctx)


def store_update_order(request, id):
    instance = Order.objects.get(id=id)
    form = OrderForm(None, instance=instance)

    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("/v1/store/requests")

    ctx = {
        'form': form
    }
    return render(request, 'store/update_order.html', ctx)
