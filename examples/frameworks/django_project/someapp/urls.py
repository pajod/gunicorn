from django.urls import path

from . import views

urlpatterns = [
    path("acsv", views.acsv),
    path("", views.home),
]
