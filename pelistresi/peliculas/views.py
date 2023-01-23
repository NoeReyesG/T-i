from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from .models import Movies, People, Directors, Ratings, Stars
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

def index(request):
    if request.method == 'POST':
        resultado = {}
        #buscarpor = request.POST["buscarpor"]
        busqueda = request.POST["buscar"]
       
        # Hacemos la query en la base de datos, aplicamos __i exact para que sea insensitivo a mayusculas y min
        # Agregamos .strip() para eliminar espacios en blanco al principio y final
        movie = Movies.objects.filter(title__icontains=busqueda.strip())
        # Si el resultado de la busqueda fue exitoso
        if movie:
            # Hacemos las busquedas necesarias en la base de datos
            movieobject = Movies.objects.get(pk=movie[0].id)
            stars = Stars.objects.filter(movie=movieobject)
            director = Directors.objects.filter(movie=movieobject)
            rating = Ratings.objects.filter(movie=movieobject)
            # Guardamos la información en un diccionario que pasaremos al front end
            resultado["id"] = movie[0].id
            resultado["titulo"] = movie[0].title
            if director:
                resultado["director"] = director[0].person.name
            else:
                resultado["director"] = "Desconocido"
            resultado["year"] = movie[0].year
            if rating:
                resultado["rating"] = rating[0].rating
                resultado["votos"] = rating[0].votes
            return render(request, "peliculas/index.html", {
                "resultado": resultado,
                "actores": stars
            })
        else:
            return render(request, "peliculas/index.html", {
            "message": "Película no encontrada",
            })
            
    else:
        #peliculas = Movies.objects.all()
        return render(request, "peliculas/index.html",{
            #"peliculas": peliculas
        })


# ruta para eliminar una película
def eliminar(request, movie_id):
    # Buscamos la película por el id que hemos pasado
    movie = Movies.objects.filter(id=movie_id)
    # Borramos la pelicula y sus relaciones por haber definido "on_delete = models.CASCADE" en el módelo.
    try:
        movie.delete()
        return render(request, "peliculas/index.html", {
                "message1": "Película eliminada con exito"
        })
    except:
        return render(request, "peliculas/index.html", {
                "message1": "¡Lo sentimos, algo salió mal!"
            })        
    
# Ruta para quitar a un actor de una película
@csrf_exempt    
def eliminar_star(request, person_id, movie_id):
    # buscamos la relación
    person = People.objects.filter(pk=person_id)
    movie = Movies.objects.filter(pk=movie_id)
    print(person[0].name)
    print(movie[0].title)
    
    return JsonResponse({
        "message2":"todo bien"
        }, status=201)

@csrf_exempt
def update(request, movie_id):
    # Buscamos la pelicula por id
    movie = Movies.objects.get(pk=movie_id)
    
    
    if request.method == "PUT":
            data = json.loads(request.body)
            if data.get("title") is not None:
                movie.title = data["title"]
            if data.get("director") is not None:
                # Buscamos si el director ya existe en nuestra base de datos 
                person = People.objects.filter(name__iexact=data["director"])
                if person:
                    person = person[0]
                    person.name = data["director"]
                    print("1")
                    print(person)
                # Si no existe lo agregamos
                else:
                    #Completar aquí mañana
                    person = People(name=data["director"])
                    print("2")
                    print(person.name)
                #person.save()
            movie.save()
            return HttpResponse(status=204)

# Ruta para nuevo registro de película
def registrar_pelicula(request):
    # Por hacer
    return render(request, "peliculas/registrar_pelicula.html")


# Ruta para nuevo registro de actor/director
def registrar_persona(request):
    # Por completar
    if request.method == 'POST':
        name = request.POST["nombre"]
        year = request.POST["year"]
        print(name)
        print(year)
        return HttpResponseRedirect(reverse("index"))
    else:    
        return render(request, "peliculas/registrar_persona.html")

# Este es el back-end para una api para autocompletar. Fue cuando traté de abordar de forma distinta el problema
# aún no estoy seguro si me servirá
@csrf_exempt
def buscar(request, busquedapor):
    if busquedapor == "titulo":
        titulos = Movies.objects.all()
        titulos = titulos.order_by("title").all()
        return JsonResponse([titulo.serialize() for titulo in titulos], safe=False)
    if busquedapor == "actor":
        actores = Stars.objects.all()
        return JsonResponse([actor.serialize() for actor in actores], safe=False)
    if busquedapor == "director":
        directores = Directors.objects.all()
        return JsonResponse([director.serialize() for director in directores], safe=False)
        
