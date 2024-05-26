from django.shortcuts import render

from .models import Table,Restaurant


 #Create your views here
def tishmanage(request):
    all_items=Restaurant.objects.all()
    return render(request, 'tischverwaltung.html',{'all_items':all_items})


def anzeigen(request):
    all_kunde=Table.objects.all()
    return render(request, 'anzeige.html',{'all_kunde':all_kunde})