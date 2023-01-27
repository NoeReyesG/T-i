from django.urls import path
from . import views

# Rutas creadas para la aplicación.
urlpatterns = [
    path("", views.index, name="index"),
    path("registrarpelicula", views.registrar_pelicula, name="registrarpelicula"),
    path("registrarpersona", views.registrar_persona, name="registrarpersona"),

    #apis
    path("eliminar/<int:movie_id>", views.eliminar, name="eliminar"),
    path("eliminar_star/<int:person_id>/<int:movie_id>", views.eliminar_star, name="eliminar_star"),
    path("update/<int:movie_id>", views.update, name="update"),
    path("buscar_persona/<str:role>/<str:name>", views.buscar_persona, name="buscar_persona"),
    path("agregar_actor/<int:movie_id>", views.agregar_actor, name="agregar_actor")
]