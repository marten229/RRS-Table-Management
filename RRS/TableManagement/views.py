from django.urls import reverse
from django.shortcuts import render
from .models import Restaurant, RestaurantLogin,Table

def tishmanage(request):
    all_items=Restaurant.objects.all()
    all_logins=RestaurantLogin.objects.all()
    return render(request, 'tischverwaltung.html', {
        'all_items': all_items,
        'all_logins': all_logins
    }
    )
selected_restaurant_name = "Losteria"  # Manuel ausgewählter Restaurantname
selected_login = RestaurantLogin.objects.filter(name=selected_restaurant_name).first()

def anzeigen(request):
    return render(request, 'anzeige.html', {'selected_login': selected_login})

def tisch_details(request):
    # Hier fügst du die Logik hinzu, um zu überprüfen, ob der Tisch belegt ist oder nicht
    return render(request, 'tisch_details.html')