from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("registrarpelicula", views.registrar_pelicula, name="registrarpelicula"),
    path("registrarpersona", views.registrar_persona, name="registrarpersona")
]