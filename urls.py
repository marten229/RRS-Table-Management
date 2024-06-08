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
from TableManagement.views import tishmanage,anzeigen,tisch_details_one,tisch_details_two,tisch_details_three,tisch_details_four,all_tables,all_tish
urlpatterns = [
    path('tischverwaltung/',tishmanage),
    path('anzeige/', anzeigen,name='anzeigen'), 
    path('details1/', tisch_details_one,name='tisch_details1'),
    path('details2/', tisch_details_two,name='tisch_details2'), 
    path('details3/', tisch_details_three,name='tisch_details3'),  
    path('details4/', tisch_details_four,name='tisch_details4'),  
    path('all-tables/', all_tables, name='all_tables'),
    path('all-tish/', all_tish, name='all_tish'),
]
