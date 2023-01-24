from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from .models import Movies, People, Directors, Ratings, Stars
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

def index(request):
    if request.method == 'POST':
        resultado = []
        
        #buscarpor = request.POST["buscarpor"]
        busqueda = request.POST["buscar"]
       
        # Hacemos la query en la base de datos, aplicamos __i exact para que sea insensitivo a mayusculas y min
        # Agregamos .strip() para eliminar espacios en blanco al principio y final
        # limitamos el resultado a los primeros 5 elementos
        movies = Movies.objects.filter(title__icontains=busqueda.strip())[:5]
      
        # Si el resultado de la busqueda fue exitoso
        list1 = []
        for movie in movies:
            dict2 = {}
            list2 = []
            list3 = []
            # Hacemos las busquedas necesarias en la base de datos
            stars = Stars.objects.filter(movie=movie)
            director = Directors.objects.filter(movie=movie)
            rating = Ratings.objects.filter(movie=movie)
            # Guardamos la información en un diccionario que pasaremos al front end
            for star in stars:
                star = star.serialize()
                list3.append(star)
            dict2["id"] = movie.id
            dict2["titulo"] = movie.title
            if director:  
                dict2["director"] = director[0].person.name
            else:
                dict2["director"] = "Desconocido"
            dict2["year"] = movie.year
            if rating:
                dict2["rating"] = rating[0].rating
                dict2["votos"] = rating[0].votes

            list2.append(dict2)
            list2.append(list3)
            list1.append(list2)

        return render(request, "peliculas/index.html", {
            "resultados": list1,
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
                "error": "¡Lo sentimos, algo salió mal!"
            })        
    
# Ruta para quitar a un actor de una película
@csrf_exempt    
def eliminar_star(request, person_id, movie_id):
    # buscamos la relación
    if request.method == 'PUT':
        person = People.objects.get(pk=person_id)
        movie = Movies.objects.get(pk=movie_id)
        # Buscamos la relacion de pelicula persona como actores
        
        star = Stars.objects.filter(movie=movie, person=person)
        #for star in stars:
        #    if (star.person == person):
        #        star1 = star
        star.delete()
        print("noe")
        return JsonResponse({
            "message":"Eliminado con exito"
            }, status=204)
    else:
        return JsonResponse({
            "error": "Se requiere PUT request"
        }, status=400)



@csrf_exempt
def update(request, movie_id):
    # Buscamos la pelicula por id y al director de dicha peli
    movie = Movies.objects.get(pk=movie_id)
    try:
        director = Directors.objects.get(movie=movie)
    except:
        return JsonResponse({
            "error": "director no encontrado"
        }, status=400)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("title") is not None:
            movie.title = data["title"]
        if data.get("director") is not None:
            # Buscamos si el director ya existe en nuestra base de datos 
            person = People.objects.filter(name__iexact=data["director"])
            if person.exists():
                person = person[0]
                director.person = person
                director.save()
            # Si no existe lo agregamos
            else:
                person = People(name=data["director"])
                print("2")
                print(person.name)
                person.save()
                director.person = person
                director.save()     
        movie.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "Se requiere PUT request"
        }, status=400)

        


@csrf_exempt
# Función para buscar actor
def buscar_actor(request, actor_name):
    actors = People.objects.filter(name__icontains=actor_name.strip())[:3]
    #actors = actors.order_by("name").all()
    return JsonResponse([actor.serialize() for actor in actors], safe=False)

@csrf_exempt
def agregar_actor(request, movie_id):
    
    if request.method == "PUT":
        movie = Movies.objects.get(pk=movie_id)
        data = json.loads(request.body)
        if data.get("person") is not None:
            person = People.objects.filter(name__iexact=data["person"])
            person = person[0]
            print(person)    
        if person:
            star = Stars(movie=movie, person=person)
            star.save()
        return JsonResponse({"message": "Agregado exitosamente"}, status=204)
    else:
        return JsonResponse({
            "error": "Se requiere PUT request"
        }, status=400)


# Función para nuevo registro de película
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
        movies = Movies.objects.all()
        movies = movies.order_by("title").all()
        return JsonResponse([movie.serialize() for movie in movies], safe=False)
    if busquedapor == "actor":
        actores = Stars.objects.all()
        return JsonResponse([actor.serialize() for actor in actores], safe=False)
    if busquedapor == "director":
        directores = Directors.objects.all()
        return JsonResponse([director.serialize() for director in directores], safe=False)
        
