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
from users import views

app_name="users"

urlpatterns = [
    path('admin_register/', views.admin_register, name='admin_register'),
    path('doctor_register/', views.doctor_register, name='doctor_register'),
    path('patient_register/', views.patient_register, name='patient_register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),


]

