from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import RestaurantLogin, Table, SeatingPlan, StaffSchedule
from django.utils import timezone
from RestaurantManagement.models import Restaurant
from ReservationManagement.models import Reservation
from UserManagement.models import User
from datetime import timedelta
import datetime
from django.http import JsonResponse
from datetime import datetime, date, time, timedelta
import logging

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

def all_tish(request, pk):
    today = timezone.now().date()
    selected_restaurant = get_object_or_404(Restaurant, pk=pk)
    table_status = []

    if selected_restaurant:
        all_tables = Table.objects.filter(restaurant=selected_restaurant)

        #for table_number in range(1, restaurant_count+1):
        #    is_occupied = all_tables.filter(table_number=table_number, date__gte=today).exists()
        #    status = 'Besetzt' if is_occupied else 'Verfügbar'
        #    table_status.append({'table_number': table_number, 'status': status})
    else:
        selected_restaurant = None

    return render(request, 'alltish.html', {'table_status': table_status, 'selected_restaurant': selected_restaurant})

def create_seating_plan(restaurant, date):
    reservations = Reservation.objects.filter(restaurant=restaurant, datum=date).order_by('uhrzeit')
    tables = Table.objects.filter(restaurant=restaurant)
    seating_plans = []

    for reservation in reservations:
        allocated = False
        for table in tables:
            if table.size >= reservation.anzahl_an_gästen:
                start_time = reservation.uhrzeit
                end_time = (datetime.combine(date, reservation.uhrzeit) + timedelta(minutes=reservation.dauer)).time()
                seating_plan = SeatingPlan(
                    restaurant=restaurant,
                    table=table,
                    reservation=reservation,
                    start_time=start_time,
                    end_time=end_time
                )
                seating_plan.save()
                seating_plans.append(seating_plan)
                allocated = True
                break
        if not allocated:
            print(f"Could not allocate table for reservation: {reservation}")

    return seating_plans

def create_staff_schedule(restaurant, date):
    reservations = Reservation.objects.filter(restaurant=restaurant, datum=date)
    staff_members = User.objects.filter(role='restaurant_staff', restaurants=restaurant)
    staff_schedules = []

    total_customers = sum([r.anzahl_an_gästen for r in reservations])
    num_staff_needed = max(1, total_customers // 10)

    shift_start = datetime.combine(date, time(18, 0))
    shift_end = datetime.combine(date, time(23, 0))

    for i in range(num_staff_needed):
        if i < len(staff_members):
            staff_schedule = StaffSchedule(
                restaurant=restaurant,
                staff=staff_members[i],
                shift_start=shift_start,
                shift_end=shift_end
            )
            staff_schedule.save() 
            staff_schedules.append(staff_schedule)

    return staff_schedules

def generate_and_view_plans(request, pk):
    restaurant = get_object_or_404(Restaurant, id=pk)
    date = timezone.now().date()

    seating_plans = []
    staff_schedules = []

    if request.method == "POST":
        if SeatingPlan.objects.filter(restaurant=restaurant, reservation__datum=date).exists() or StaffSchedule.objects.filter(restaurant=restaurant, shift_start__date=date).exists():
            SeatingPlan.objects.filter(restaurant=restaurant, reservation__datum=date).delete()
            StaffSchedule.objects.filter(restaurant=restaurant, shift_start__date=date).delete()
        seating_plans = create_seating_plan(restaurant, date)
        staff_schedules = create_staff_schedule(restaurant, date)
    elif request.method == "GET":
        seating_plans = SeatingPlan.objects.filter(restaurant=restaurant, reservation__datum=date)
        staff_schedules = StaffSchedule.objects.filter(restaurant=restaurant, shift_start__date=date)

    context = {
        'restaurant': restaurant,
        'date': date,
        'seating_plans': seating_plans,
        'staff_schedules': staff_schedules,
    }
    return render(request, 'generate_and_view_plans.html', context)


def table_list(request, restaurant_id):
    tables = Table.objects.filter(restaurant_id=restaurant_id)
    return render(request, 'table_list.html', {'tables': tables})

def table_detail(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    reservations = SeatingPlan.objects.filter(table=table).select_related('reservation')

    table_availability = table.is_available()

    #logger.debug(f"Table {table.id} availability in view: {table_availability}")
    print(f"Table {table.id} availability in view: {table_availability}")

    return render(request, 'table_detail.html', {
        'table': table,
        'reservations': reservations,
        'is_available': table_availability
    })