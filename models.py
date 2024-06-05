from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    table_number = models.IntegerField()

    def __str__(self):
        return self.name
    
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
    kunde = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    guests = models.IntegerField()
    special_requests = models.TextField(blank=True)
    table_number = models.IntegerField()

    def __str__(self):
        return f"Reservation for {self.kunde} at {self.restaurant.name} on {self.date} at {self.time}"
