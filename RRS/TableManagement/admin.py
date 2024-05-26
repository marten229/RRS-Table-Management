from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Table,Restaurant


admin.site.register(Table)
admin.site.register(Restaurant)