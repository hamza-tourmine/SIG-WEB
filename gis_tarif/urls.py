from django.urls import path
from . import views

urlpatterns = [
    path("", views.carte_view, name="carte"),
    path("api/bois/calcul/", views.calcul_volume_bois, name="calcul_volume_bois"),
    path(
        "api/liege/calcul/",
        views.calcul_rendement_liege,
        name="calcul_rendement_liege",
    ),
]
