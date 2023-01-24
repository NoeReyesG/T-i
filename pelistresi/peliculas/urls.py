from django.urls import path
from . import views

# Rutas creadas para la aplicación.
urlpatterns = [
    path("", views.index, name="index"),
    path("registrarpelicula", views.registrar_pelicula, name="registrarpelicula"),
    path("registrarpersona", views.registrar_persona, name="registrarpersona"),

    #api
    path("buscar/<str:busquedapor>", views.buscar, name="buscar"),
    path("eliminar/<int:movie_id>", views.eliminar, name="eliminar"),
    path("eliminar_star/<int:person_id>/<int:movie_id>", views.eliminar_star, name="eliminar_star"),
    path("update/<int:movie_id>", views.update, name="update"),
    path("buscar_actor/<str:actor_name>", views.buscar_actor, name="buscar_actor")
]