from django.shortcuts import render, get_object_or_404, redirect
from .models import Table, SeatingPlan, StaffSchedule
from django.utils import timezone
from RestaurantManagement.models import Restaurant
from ReservationManagement.models import Reservation
from UserManagement.models import User
import datetime
from datetime import datetime, time, timedelta
from .forms import AssignReservationForm
from django.contrib.auth.decorators import login_required
from UserManagement.decorators import role_and_restaurant_required

def create_seating_plan(restaurant, date):
    reservations = Reservation.objects.filter(restaurant=restaurant, datum=date).order_by('uhrzeit')
    tables = Table.objects.filter(restaurant=restaurant, is_active=True) 
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

    shift_start = datetime.combine(date, restaurant.opening_time)
    shift_end = datetime.combine(date, restaurant.closing_time)

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

@login_required
@role_and_restaurant_required(['administrator', 'restaurant_owner', 'restaurant_staff'])
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

@login_required
@role_and_restaurant_required(['administrator', 'restaurant_owner', 'restaurant_staff'])
def table_list(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    tables = Table.objects.filter(restaurant=restaurant)
    return render(request, 'table_list.html', {'tables': tables, 'restaurant': restaurant})

@login_required
@role_and_restaurant_required(['administrator', 'restaurant_owner', 'restaurant_staff'])
def table_detail(request, pk, table_id):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    table = get_object_or_404(Table, id=table_id)
    current_time = timezone.now()
    reservations = SeatingPlan.objects.filter(
        table=table,
        reservation__datum__gte=current_time.date(),
        start_time__gte=current_time.time()
    ).select_related('reservation')

    table_availability = table.is_available()

    if request.method == 'POST':
        if 'assign_reservation' in request.POST:
            form = AssignReservationForm(request.POST)
            if form.is_valid():
                existing_reservation = form.cleaned_data.get('vorhandene_reservierung')
                if existing_reservation:
                    reservation = existing_reservation
                else:
                    reservation = Reservation.objects.create(
                        restaurant=table.restaurant,
                        name=form.cleaned_data.get('neue_reservierung_name'),
                        email=form.cleaned_data.get('neue_reservierung_email'),
                        telefon_nummer=form.cleaned_data.get('neue_reservierung_telefon'),
                        datum=form.cleaned_data.get('neue_reservierung_datum'),
                        uhrzeit=form.cleaned_data.get('neue_reservierung_uhrzeit'),
                        dauer=form.cleaned_data.get('neue_reservierung_dauer'),
                        anzahl_an_gästen=form.cleaned_data.get('neue_reservierung_gaeste')
                    )

                seating_plan = SeatingPlan.objects.create(
                    restaurant=table.restaurant,
                    table=table,
                    reservation=reservation,
                    start_time=reservation.uhrzeit,
                    end_time=(datetime.combine(datetime.min, reservation.uhrzeit) + timedelta(minutes=reservation.dauer)).time()
                )
                return redirect('table_detail', pk=restaurant.id, table_id=table.id)
        elif 'remove_reservation' in request.POST:
            seating_plan_id = request.POST.get('seating_plan_id')
            seating_plan = get_object_or_404(SeatingPlan, id=seating_plan_id)
            seating_plan.delete()
            return redirect('table_detail', pk=restaurant.id, table_id=table.id)
        elif 'toggle_table_status' in request.POST:
            table.is_active = not table.is_active
            table.save()
            return redirect('table_detail', pk=restaurant.id, table_id=table.id)
    else:
        form = AssignReservationForm()

    return render(request, 'table_detail.html', {
        'table': table,
        'reservations': reservations,
        'is_available': table_availability,
        'form': form,
        'restaurant': restaurant
    })