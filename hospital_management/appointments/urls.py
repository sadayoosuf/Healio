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
from appointments import views

app_name="appointments"

urlpatterns = [
    path('appointmentbook/', views.book_appointment, name='book_appointment'),
    path('history/', views.appointment_history, name='appointment_history'),
    path('doctor/appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('edit/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),
    path('delete/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),



]

