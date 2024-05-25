from django import forms
from django.forms import ModelForm
from .models import Table

class TableForm(ModelForm):
    class Meta:
        model=Table
        fields = ['name', 'email', 'phone', 'date', 'time', 'guests', 'special_requests']  # Auch hier 'spezial_request' zu 'special_requests' ändern