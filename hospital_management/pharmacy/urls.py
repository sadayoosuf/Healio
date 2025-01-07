"""
URL configuration for hospital_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.urls import path
from pharmacy import views

app_name="pharmacy"

urlpatterns = [
    path('category/', views.allcategories, name='category'),
    path('medicines/<int:m>',views.allmedicines,name="medicines"),
    path('medicinesdetail/<int:m>', views.medicinesdetails, name="medicinesdetail"),
    path('addcat',views.addcategory,name="addcat"),
    path('addmedicine',views.addmedicine,name="addmed"),
    path('addtocart/<int:i>', views.add_to_cart, name="addtocart"),
    path('cartview',views.cart_view,name="cartview"),
    path('cartremove/<int:i>',views.cart_remove,name="cartremove"),
    path('cartdelete/<int:i>',views.cart_delete,name="cartdelete"),
    path('orderform',views.order_form,name="orderform"),
    path('status/<u>',views.payment_status,name="status"),
    path('orderview',views.order_view,name="orderview"),
    path('addstock/<int:m>',views.add_stock,name="addstock"),
    path('search/', views.search_medicine, name="search"),


]

