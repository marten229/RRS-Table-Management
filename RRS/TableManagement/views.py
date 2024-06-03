from django.urls import reverse
from django.shortcuts import render
from .models import Restaurant, RestaurantLogin,Table
from django.utils import timezone

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


today = timezone.now().date()

def tisch_details_one(request):
    # Hier fügst du die Logik hinzu, um zu überprüfen, ob der Tisch belegt ist oder nicht
     # Heutiges Datum
    kunden = Table.objects.filter(guests__lte=4, date__gte=today)
    selected_restaurant_name = "Losteria"
    selected_login = RestaurantLogin.objects.filter(name=selected_restaurant_name).first()
    return render(request, 'tisch_details1.html', {'kunden': kunden, 'selected_login':selected_login})

def tisch_details_two(request):
    # Hier fügst du die Logik hinzu, um zu überprüfen, ob der Tisch belegt ist oder nicht
    kunden = Table.objects.filter(guests__gt=4, guests__lte=6,date__gte=today)  # Filtern nach Tischen mit 5-6 Gästen
    selected_restaurant_name = "Losteria"  # Manuel ausgewählter Restaurantname
    selected_login = RestaurantLogin.objects.filter(name=selected_restaurant_name).first()
    return render(request, 'tisch_details2.html', {'kunden': kunden, 'selected_login': selected_login})

def tisch_details_three(request):
    # Hier fügst du die Logik hinzu, um zu überprüfen, ob der Tisch belegt ist oder nicht
    kunden = Table.objects.filter(guests__gt=6, guests__lte=8,date__gte=today)  # Filtern nach Tischen mit 5-6 Gästen
    selected_restaurant_name = "Losteria"  # Manuel ausgewählter Restaurantname
    selected_login = RestaurantLogin.objects.filter(name=selected_restaurant_name).first()
    return render(request, 'tisch_details3.html', {'kunden': kunden, 'selected_login': selected_login})

def tisch_details_four(request):
    kunden = Table.objects.filter(guests__gt=8,date__gte=today)  # Filtern nach Tischen mit mehr als 8 Gästen
    selected_restaurant_name = "Losteria"  # Manuel ausgewählter Restaurantname
    selected_login = RestaurantLogin.objects.filter(name=selected_restaurant_name).first()
    return render(request, 'tisch_details4.html', {'kunden': kunden, 'selected_login': selected_login})

def all_tables(request):
    selected_restaurant_name = "Losteria"
    kunden = Table.objects.all()
    selected_login = RestaurantLogin.objects.filter(name=selected_restaurant_name).first()
    return render(request, 'all_tables.html', {'kunden': kunden, 'selected_login': selected_login})



def all_tish(request):
    selected_restaurant_name = "Losteria"
    selected_restaurant = Restaurant.objects.filter(name=selected_restaurant_name).first()
    table_status = []
    restaurant_count = Restaurant.objects.count()
    if selected_restaurant:
        # Alle Tische des Restaurants
        all_tables = selected_restaurant.table_set.all()

        # Durchgehen aller Tischnummern des Restaurants
        for table_number in range(1, restaurant_count+1):
            # Überprüfen, ob dieser Tisch in der Table-Tabelle besetzt ist
            is_occupied = all_tables.filter(table_number=table_number, date__gte=today).exists()
            status = 'Besetzt' if is_occupied else 'Verfügbar'
            table_status.append({'table_number': table_number, 'status': status})
    else:
        selected_restaurant = None

    return render(request, 'alltish.html', {'table_status': table_status, 'selected_restaurant': selected_restaurant})




