from django.urls import path
from . import views

urlpatterns = [
    path("localities/", views.get_localities, name="admin_localities"),
    path("areas/", views.get_areas, name="admin_areas"),
]