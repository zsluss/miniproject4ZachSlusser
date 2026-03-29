from django.conf import settings
from django.db import migrations
from django.utils import timezone


def seed_initial_weather_data(apps, schema_editor):
    UserModel = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
    Zip = apps.get_model("weather", "Zip")
    WeatherData = apps.get_model("weather", "WeatherData")

    seed_user, created = UserModel.objects.get_or_create(
        username="sample_weather_user",
        defaults={"email": "sample@example.com"},
    )
    if created:
        seed_user.set_unusable_password()
        seed_user.save(update_fields=["password"])

    now = timezone.now()
    seed_rows = [
        {"zipcode": "67601", "temperature": 72.0, "humidity": 41.0, "condition": "Partly cloudy"},
        {"zipcode": "67202", "temperature": 68.0, "humidity": 56.0, "condition": "Clear"},
        {"zipcode": "66044", "temperature": 70.0, "humidity": 49.0, "condition": "Sunny"},
    ]

    for row in seed_rows:
        zip_entry, _ = Zip.objects.get_or_create(
            user=seed_user,
            zipcode=row["zipcode"],
            defaults={"pub_date": now},
        )

        WeatherData.objects.get_or_create(
            zip_search=zip_entry,
            condition=row["condition"],
            temperature=row["temperature"],
            humidity=row["humidity"],
            defaults={"pub_date": now},
        )


def remove_initial_weather_data(apps, schema_editor):
    UserModel = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
    Zip = apps.get_model("weather", "Zip")
    WeatherData = apps.get_model("weather", "WeatherData")

    seed_username = "sample_weather_user"
    seed_zipcodes = ["67601", "67202", "66044"]

    seed_user = UserModel.objects.filter(username=seed_username).first()
    if not seed_user:
        return

    zip_ids = list(
        Zip.objects.filter(user=seed_user, zipcode__in=seed_zipcodes).values_list("id", flat=True)
    )
    if zip_ids:
        WeatherData.objects.filter(zip_search_id__in=zip_ids).delete()

    Zip.objects.filter(user=seed_user, zipcode__in=seed_zipcodes).delete()

    if not Zip.objects.filter(user=seed_user).exists():
        seed_user.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("weather", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_initial_weather_data, remove_initial_weather_data),
    ]
