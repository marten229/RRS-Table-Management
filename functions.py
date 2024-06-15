from django.utils import timezone
from .models import Table, SeatingPlan
from datetime import datetime, timedelta


def is_a_table_available(restaurant):
    now = timezone.localtime()
    current_date = now.date()
    current_time = now.time()
    available_tables = Table.objects.filter(
        restaurant=restaurant
    ).exclude(
        seatingplan__reservation__datum=current_date,
        seatingplan__start_time__lte=current_time,
        seatingplan__end_time__gte=current_time
    )

    if available_tables.exists():
        return current_time

    next_available_time = None
    future_reservations = SeatingPlan.objects.filter(
        table__restaurant=restaurant,
        reservation__datum__gte=current_date
    ).order_by('reservation__datum', 'start_time')

    for reservation in future_reservations:
        if reservation.reservation.datum == current_date and reservation.start_time <= current_time:
            continue

        if next_available_time is None:
            next_available_time = reservation.end_time + timedelta(minutes=1)
            break

    if next_available_time:
        return next_available_time

    return None

def is_a_table_available_with_size(restaurant, date, time, duration, party_size):
    now = timezone.localtime()
    current_date = now.date()
    current_time = now.time()
    available_tables = Table.objects.filter(
        restaurant=restaurant
    ).exclude(
        seatingplan__reservation__datum=current_date,
        seatingplan__start_time__lte=current_time,
        seatingplan__end_time__gte=current_time
    )

    if available_tables.exists():
        return current_time
    
def is_a_table_available_with_size(restaurant, date, time, duration, party_size):
    reservation_start = datetime.combine(date, time)
    reservation_end = reservation_start + timedelta(hours=duration)

    available_tables = Table.objects.filter(
        restaurant=restaurant,
        size__gte=party_size
    ).exclude(
        seatingplan__reservation__datum=date,
        seatingplan__start_time__lt=reservation_end.time(),
        seatingplan__end_time__gt=reservation_start.time()
    )

    return available_tables