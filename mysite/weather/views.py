import asyncio

import python_weather
from django.shortcuts import render
from django.utils import timezone
from .forms import WeatherSearchForm
from .models import Name, WeatherData, Zip


async def _fetch_weather(zipcode):
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        forecast = await client.get(zipcode)
        return {
            "temperature": forecast.temperature,
            "humidity": forecast.humidity,
            "condition": forecast.description,
        }


def index(request):
    weather_result = None

    if request.method == "POST":
        form = WeatherSearchForm(request.POST)
        if form.is_valid():
            zipcode = form.cleaned_data["zipcode"]

            try:
                weather_result = asyncio.run(_fetch_weather(zipcode))
            except Exception:
                form.add_error(None, "Could not fetch weather right now. Please try again.")
            else:
                name_entry = Name.objects.create(
                    name=form.cleaned_data["name"],
                    pub_date=timezone.now(),
                )
                zip_entry = Zip.objects.create(
                    name=name_entry,
                    zipcode=zipcode,
                    pub_date=timezone.now(),
                )
                WeatherData.objects.create(
                    zip=zip_entry,
                    temperature=weather_result["temperature"],
                    humidity=weather_result["humidity"],
                    condition=weather_result["condition"],
                    pub_date=timezone.now(),
                )
    else:
        form = WeatherSearchForm()

    return render(
        request,
        "weather/index.html",
        {
            "form": form,
            "weather_result": weather_result,
        },
    )
