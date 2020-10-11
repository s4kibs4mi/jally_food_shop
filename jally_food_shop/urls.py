"""jally_food_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_api import views

urlpatterns = [
                  path('v1/', views.overview),
                  path('v1/register/', views.users_register),
                  path('v1/login/', views.users_login),
                  path('v1/users/', views.users_profile),
                  path('v1/orders/create/', views.orders_create),
                  path('v1/orders/search/', views.orders_list),
                  path('v1/orders/view/<str:id>/', views.orders_get),
                  path('v1/products/search/', views.products_list),

                  path('v1/store/', views.store_home),
                  path('v1/store/products/', views.store_list_products),
                  path('v1/store/products/new/', views.store_add_product),
                  path('v1/store/products/update/<str:id>/', views.store_update_product),
                  path('v1/store/products/delete/<str:id>/', views.store_delete_product),

                  path('v1/store/categories/new/', views.store_add_food_category),
                  path('v1/store/categories/', views.store_list_categories),
                  path('v1/store/categories/update/<str:id>/', views.store_update_category),
                  path('v1/store/categories/delete/<str:id>/', views.store_delete_category),

                  path('admin/', admin.site.urls),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
