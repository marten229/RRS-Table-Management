from django.db import models
from RestaurantManagement.models import Restaurant
from ReservationManagement.models import Reservation
    
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
    reservation=models.ForeignKey(Reservation, on_delete=models.CASCADE)
    table_number = models.IntegerField()
    size = models.IntegerField()
    count=models.IntegerField()
