"""
URL configuration for RRS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from TableManagement import views
urlpatterns = [
    path('generate_and_view_plans/<int:pk>/', views.generate_and_view_plans, name='generate_and_view_plans'),
    path('restaurants/<int:restaurant_id>/tables/', views.table_list, name='table_list'),
    path('tables/<int:table_id>/', views.table_detail, name='table_detail'),
]
