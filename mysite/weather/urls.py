from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("my-searches/", views.my_searches, name="my_searches"),
    path("search/", views.index, name="index"),
]