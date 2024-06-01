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

def tisch_details_one(request):
    # Hier fügst du die Logik hinzu, um zu überprüfen, ob der Tisch belegt ist oder nicht
    kunden = Table.objects.filter(guests__lte=4)
    selected_restaurant_name = "Losteria"  # Manuel ausgewählter Restaurantname
    selected_login = RestaurantLogin.objects.filter(name=selected_restaurant_name).first()
    return render(request, 'tisch_details1.html', {'kunden': kunden, 'selected_login':selected_login})

def tisch_details_two(request):
    # Hier fügst du die Logik hinzu, um zu überprüfen, ob der Tisch belegt ist oder nicht
    kunden = Table.objects.filter(guests__gt=4, guests__lte=6)  # Filtern nach Tischen mit 5-6 Gästen
    selected_restaurant_name = "Losteria"  # Manuel ausgewählter Restaurantname
    selected_login = RestaurantLogin.objects.filter(name=selected_restaurant_name).first()
    return render(request, 'tisch_details2.html', {'kunden': kunden, 'selected_login': selected_login})

def tisch_details_three(request):
    # Hier fügst du die Logik hinzu, um zu überprüfen, ob der Tisch belegt ist oder nicht
    kunden = Table.objects.filter(guests__gt=6, guests__lte=8)  # Filtern nach Tischen mit 5-6 Gästen
    selected_restaurant_name = "Losteria"  # Manuel ausgewählter Restaurantname
    selected_login = RestaurantLogin.objects.filter(name=selected_restaurant_name).first()
    return render(request, 'tisch_details3.html', {'kunden': kunden, 'selected_login': selected_login})

def tisch_details_four(request):
    kunden = Table.objects.filter(guests__gt=8)  # Filtern nach Tischen mit mehr als 8 Gästen
    selected_restaurant_name = "Losteria"  # Manuel ausgewählter Restaurantname
    selected_login = RestaurantLogin.objects.filter(name=selected_restaurant_name).first()
    return render(request, 'tisch_details4.html', {'kunden': kunden, 'selected_login': selected_login})