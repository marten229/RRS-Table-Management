from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import RestaurantLogin,Table,Reservation

admin.site.register(Table)
admin.site.register(RestaurantLogin)
admin.site.register(Reservation)
