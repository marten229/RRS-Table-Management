from django.shortcuts import render
from django.shortcuts import render, redirect
from django import forms
from .forms import TableForm
from .models import Table


# Create your views here
def tishmanage(request):
    return render(request, 'tischverwaltung.html')

def success_view(request):
    return render(request, 'success.html')