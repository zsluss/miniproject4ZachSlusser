from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import WeatherSearchForm
from .models import Name, Zip


def index(request):
    if request.method == "POST":
        form = WeatherSearchForm(request.POST)
        if form.is_valid():
            name_entry = Name.objects.create(
                name=form.cleaned_data["name"],
                pub_date=timezone.now(),
            )
            Zip.objects.create(
                name=name_entry,
                zipcode=form.cleaned_data["zipcode"],
                pub_date=timezone.now(),
            )
            return redirect("index")
    else:
        form = WeatherSearchForm()

    return render(request, "weather/index.html", {"form": form})
