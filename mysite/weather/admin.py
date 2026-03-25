from django.contrib import admin
from .models import Zip, WeatherData


@admin.register(Zip)
class ZipAdmin(admin.ModelAdmin):
	list_display = ("user", "zipcode", "pub_date")
	search_fields = ("zipcode", "user__username")
	list_filter = ("pub_date",)


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
	list_display = ("zip_search", "temperature", "humidity", "condition", "pub_date")
	search_fields = ("zip_search__zipcode", "condition")
	list_filter = ("condition", "pub_date")
