from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.shortcuts import redirect
from rest_api.forms import FoodItemForm
from rest_api.forms import FoodCategoryForm
from rest_api.models import FoodItem


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
    pass


@api_view(['POST'])
def users_login(request):
    pass


@api_view(['GET'])
def users_profile(request):
    pass


@api_view(['POST'])
def orders_create(request):
    pass


@api_view(['GET'])
def orders_get(request):
    pass


@api_view(['GET'])
def orders_list(request):
    pass


def store_home(request):
    return render(request, 'store/index.html')


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
    food_items = FoodItem.objects.all()
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
