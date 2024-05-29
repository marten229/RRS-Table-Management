from django.shortcuts import render

from .models import Table,Restaurant,RestaurantLogin


 #Create your views here
def tishmanage(request):
    all_items=Restaurant.objects.all()
    all_logins=RestaurantLogin.objects.all()
    return render(request, 'tischverwaltung.html', {
        'all_items': all_items,
        'all_logins': all_logins
    })
def anzeigen(request):
    all_kunde=Table.objects.all()
    all_logins=RestaurantLogin.objects.all()
    return render(request, 'anzeige.html',{
        'all_kunde':all_kunde,
        'all_logins': all_logins
    })