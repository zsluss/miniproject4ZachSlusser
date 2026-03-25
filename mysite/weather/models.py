from django.db import models

# Create your models here..

class Name(models.Model):
    name = models.CharField(max_length=50)
    pub_date = models.DateTimeField("time checked")


class Zip(models.Model):
    name = models.ForeignKey(Name, on_delete=models.CASCADE)
    zipcode = models.CharField(max_length=5)
    pub_date = models.DateTimeField("time checked")

class WeatherData(models.Model):
    zip = models.ForeignKey(Zip, on_delete=models.CASCADE)
    temperature = models.FloatField()
    humidity = models.FloatField()
    condition = models.CharField(max_length=100)
    pub_date = models.DateTimeField("time recorded")