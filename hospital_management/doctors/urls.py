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
from doctors import views

app_name="doctors"

urlpatterns = [
    path('',views.alldepartments,name="department"),
    path('doctor/<int:d>',views.alldoctors,name="doctor"),
    path('doctorsdetail/<int:d>',views.doctorsdetails,name="doctorsdetail"),
    path('service/',views.service,name="service"),
    path('adddepartment',views.add_department,name="add_department"),
    path('adddoctor',views.add_doctor,name="add_doctor"),
    path('searchdoctor/', views.search_doctor, name="searchdoctor"),
    path('edit-department/<int:id>/', views.edit_department, name="edit_department"),
    path('delete-department/<int:id>/', views.delete_department, name="delete_department"),


]

