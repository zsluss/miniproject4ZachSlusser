from django.conf import settings
from django.db import models

# Create your models here..


class Zip(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    zipcode = models.CharField(max_length=5)
    pub_date = models.DateTimeField("time checked")

    def __str__(self):
        return f"{self.user.username} - {self.zipcode}"

class WeatherData(models.Model):
    zip_search = models.ForeignKey(Zip, on_delete=models.CASCADE)
    temperature = models.FloatField()
    humidity = models.FloatField()
    condition = models.CharField(max_length=100)
    pub_date = models.DateTimeField("time recorded")

    def __str__(self):
        return f"{self.zip_search.zipcode} - {self.condition}"