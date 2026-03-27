import asyncio

import python_weather
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from .forms import WeatherSearchForm
from .models import WeatherData, Zip


async def _fetch_weather(zipcode):
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        forecast = await client.get(zipcode)
        return {
            "temperature": forecast.temperature,
            "humidity": forecast.humidity,
            "condition": forecast.description,
        }


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})


def home(request):
    if request.user.is_authenticated:
        return redirect("index")

    recent_searches = (
        WeatherData.objects.select_related("zip_search", "zip_search__user")
        .order_by("-pub_date")[:3]
    )

    return render(
        request,
        "weather/home.html",
        {"recent_searches": recent_searches},
    )


def logout_view(request):
    if request.method != "POST":
        if request.user.is_authenticated:
            return HttpResponseNotAllowed(["POST"])
        return redirect_to_login(request.get_full_path())

    logout(request)
    return redirect("login")


@login_required
def my_searches(request):
    searches = (
        WeatherData.objects.select_related("zip_search", "zip_search__user")
        .filter(zip_search__user=request.user)
        .order_by("-pub_date")
    )

    return render(
        request,
        "weather/my_searches.html",
        {"searches": searches},
    )


@login_required
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
                zip_entry = Zip.objects.create(
                    user=request.user,
                    zipcode=zipcode,
                    pub_date=timezone.now(),
                )
                WeatherData.objects.create(
                    zip_search=zip_entry,
                    temperature=weather_result["temperature"],
                    humidity=weather_result["humidity"],
                    condition=weather_result["condition"],
                    pub_date=timezone.now(),
                )
    else:
        form = WeatherSearchForm()

    recent_searches = (
        WeatherData.objects.select_related("zip_search", "zip_search__user")
        .order_by("-pub_date")[:10]
    )

    return render(
        request,
        "weather/index.html",
        {
            "form": form,
            "weather_result": weather_result,
            "recent_searches": recent_searches,
        },
    )
