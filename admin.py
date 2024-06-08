from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Table,Restaurant,RestaurantLogin


admin.site.register(Table)
admin.site.register(Restaurant)
admin.site.register(RestaurantLogin)
