from django.shortcuts import render
from django.http import HttpResponse
from .models import RestaurantLogin, Table
from django.utils import timezone
from RestaurantManagement.models import Restaurant

def tishmanage(request):
    all_items = Restaurant.objects.all()
    all_logins = RestaurantLogin.objects.all()
    return render(request, 'tischverwaltung.html', {
        'all_items': all_items,
        'all_logins': all_logins
    })

def restoruantanzeigen(request):
    all_items = Restaurant.objects.all()
    return render(request, 'tischverwaltung.html', {
        'all_items': all_items,
    })

def anzeigen(request):
    selected_restaurant_name = request.GET.get('restaurant', '') # Restaurantnamen aus GET-Parameter extrahieren
    selected_login = RestaurantLogin.objects.filter(name=selected_restaurant_name).first()
    return render(request, 'anzeige.html', {'selected_login': selected_login,'selected_restaurant_name': selected_restaurant_name})

def tisch_details_one(request):
    today = timezone.now().date()
    selected_restaurant_name = request.GET.get('restaurant', '') # Restaurantnamen aus GET-Parameter extrahieren
    selected_login = RestaurantLogin.objects.filter(name=selected_restaurant_name).first()
    kunden = Table.objects.filter(guests__lte=4, date__gte=today)
    return render(request, 'tisch_details1.html', {'kunden': kunden, 'selected_login': selected_login})

def tisch_details_two(request):
    today = timezone.now().date()
    selected_restaurant_name = request.GET.get('restaurant', '') # Restaurantnamen aus GET-Parameter extrahieren
    selected_login = RestaurantLogin.objects.filter(name=selected_restaurant_name).first()
    kunden = Table.objects.filter(guests__gt=4, guests__lte=6, date__gte=today)
    return render(request, 'tisch_details2.html', {'kunden': kunden, 'selected_login': selected_login})

def tisch_details_three(request):
    today = timezone.now().date()
    selected_restaurant_name = request.GET.get('restaurant', '') # Restaurantnamen aus GET-Parameter extrahieren
    selected_login = RestaurantLogin.objects.filter(name=selected_restaurant_name).first()
    kunden = Table.objects.filter(guests__gt=6, guests__lte=8, date__gte=today)
    return render(request, 'tisch_details3.html', {'kunden': kunden, 'selected_login': selected_login})

def tisch_details_four(request):
    today = timezone.now().date()
    selected_restaurant_name = request.GET.get('restaurant', '') # Restaurantnamen aus GET-Parameter extrahieren
    selected_login = RestaurantLogin.objects.filter(name=selected_restaurant_name).first()
    kunden = Table.objects.filter(guests__gt=8, date__gte=today)
    return render(request, 'tisch_details4.html', {'kunden': kunden, 'selected_login': selected_login})

def all_tables(request):
    today = timezone.now().date()
    selected_restaurant_name = request.GET.get('restaurant', '') # Restaurantnamen aus GET-Parameter extrahieren
    selected_login = RestaurantLogin.objects.filter(name=selected_restaurant_name).first()
    kunden = Table.objects.all()
    return render(request, 'all_tables.html', {'kunden': kunden, 'selected_login': selected_login})

def all_tish(request):
    today = timezone.now().date()
    selected_restaurant_name = request.GET.get('restaurant', '') # Restaurantnamen aus GET-Parameter extrahieren
    selected_restaurant = Restaurant.objects.filter(name=selected_restaurant_name).first()
    table_status = []
    restaurant_count = Restaurant.objects.count()

    if selected_restaurant:
        all_tables = selected_restaurant.table_set.all()

        for table_number in range(1, restaurant_count+1):
            is_occupied = all_tables.filter(table_number=table_number, date__gte=today).exists()
            status = 'Besetzt' if is_occupied else 'Verfügbar'
            table_status.append({'table_number': table_number, 'status': status})
    else:
        selected_restaurant = None

    return render(request, 'alltish.html', {'table_status': table_status, 'selected_restaurant': selected_restaurant})
