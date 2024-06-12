from django.db import models
from django.utils import timezone
from RestaurantManagement.models import Restaurant
from ReservationManagement.models import Reservation
from UserManagement.models import User
from datetime import datetime, date, timedelta
import logging

#logger = logging.getLogger(__name__)
    
class RestaurantLogin(models.Model):
    name = models.CharField(max_length=100)
    Totaltable_number = models.IntegerField()
    onetofortable = models.IntegerField()
    fortoeisixtable = models.IntegerField()
    sixtoeighttable = models.IntegerField()
    morthaneight= models.IntegerField()

    
    def __str__(self):
        return self.name

class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    size = models.IntegerField()
    count = models.IntegerField()

    def is_available(self):
        now = timezone.localtime()
        current_time = now.time()
        current_date = now.date()

        overlapping_reservations = SeatingPlan.objects.filter(
            table=self,
            reservation__datum=current_date,
            start_time__lte=current_time,
            end_time__gte=current_time
        ).exists()

        return not overlapping_reservations

class SeatingPlan(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def save(self, *args, **kwargs):
        self.start_time = self.reservation.uhrzeit
        self.end_time = (datetime.combine(date.min, self.start_time) + timedelta(minutes=self.reservation.dauer)).time()
        super().save(*args, **kwargs)

class StaffSchedule(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    staff = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'restaurant_staff'})
    shift_start = models.DateTimeField()
    shift_end = models.DateTimeField()
