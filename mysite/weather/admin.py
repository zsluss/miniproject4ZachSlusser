from django.contrib import admin
from .models import Name, Zip, WeatherData


@admin.register(Name)
class NameAdmin(admin.ModelAdmin):
	list_display = ("name", "pub_date")
	search_fields = ("name",)


@admin.register(Zip)
class ZipAdmin(admin.ModelAdmin):
	list_display = ("name", "zipcode", "pub_date")
	search_fields = ("zipcode", "name__name")
	list_filter = ("pub_date",)


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
	list_display = ("zip", "temperature", "humidity", "condition", "pub_date")
	search_fields = ("zip__zipcode", "condition")
	list_filter = ("condition", "pub_date")
