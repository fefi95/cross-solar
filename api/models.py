from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Panel(models.Model):
    brand = models.CharField(max_length=200)
    # The description said it had to be exactly 16 chars
    serial = models.CharField(max_length=16)
    latitude = models.DecimalField(
        decimal_places=6, max_digits=8,
        validators=[MinValueValidator(-90), MaxValueValidator(90)]
    )
    longitude = models.DecimalField(
        decimal_places=6, max_digits=9,
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )
    def __str__(self):
        return "Brand: {0}, Serial: {1} ".format(self.brand, self.serial)

class OneHourElectricity(models.Model):
    panel = models.ForeignKey(Panel, on_delete=models.CASCADE)
    kilo_watt = models.BigIntegerField()
    date_time = models.DateTimeField()
    def __str__(self):
        return "Hour: {0} - {1} KiloWatt".format(self.date_time, self.kilo_watt)
