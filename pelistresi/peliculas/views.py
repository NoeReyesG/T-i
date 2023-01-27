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
        if not movies.exists():
            message = "Pelicula no encontrada!"
        else:
            message =""
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
            "message": message
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
    
    #try:
    #    director = Directors.objects.get(movie=movie)
    #except:
    #    director = Directors(movie=movie)
    if request.method == "PUT":
        # Buscamos la pelicula por id
        movie = Movies.objects.get(pk=movie_id)
        # cargamos los datos que se nos han pasado en el fetch (título y director)
        data = json.loads(request.body)
        if data.get("title") is not None:
            movie.title = data["title"]
            movie.save()
        if data.get("director") is not None:
            # Buscamos si el director ya existe en nuestra base de datos 
            person = People.objects.filter(name__iexact=data["director"])
            # Si existe...
            if person:
                person = person[0]
                print("1")
                print(person.name)
                #...verificamos si la película tiene director registrado 
                try:
                    director = Directors.objects.get(movie=movie)
                # si no creamos la relación
                except:
                    director = Directors(movie=movie, person=person)
                print(2)
                # Actualizamos al director
                director.person = person
                print(director.person.name)
                print(director.movie.title)
                director.save()
                return HttpResponse(status=204)
            # Si no existe el director en nuestra base de dartos mandamos un mensaje
            else:
                return JsonResponse({"message": "Director no existe"}, status = 400)
    else:
        return JsonResponse({
            "error": "Se requiere PUT request"
        }, status=400)

        


@csrf_exempt
# Función para buscar actor
def buscar_persona(request, role, name,):
    if role == "actor":
        actors = People.objects.filter(name__icontains=name.strip())[:3]
        #actors = actors.order_by("name").all()
        return JsonResponse([actor.serialize() for actor in actors], safe=False)
    if role == "director":
        director = People.objects.filter(name__iexact=name.strip())
        if director:
            return JsonResponse({"resultado": "encontrado"})
        else:
            return JsonResponse({"resultado": "no encontrado"})

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
            # Prevenimos que se agregue más de una vez, un actor que ya participa en la película.
            actor = Stars.objects.filter(movie=movie, person=person)
            if(actor):
                print("no agregado")
                return JsonResponse({"message": "actor agregado previamente"}, status=400)
            else:
                star = Stars(movie=movie, person=person)
                print(star.person.name)
                star.save()
        return JsonResponse({"message": "Agregado exitosamente"})
    else:
        return JsonResponse({
            "error": "Se requiere PUT request"
        }, status=400)


# Función para nuevo registro de película
def registrar_pelicula(request):
    # Por hacer
    if request.method == 'POST':
        title = request.POST["title"]
        year = request.POST["year"]
        person = request.POST["director"]
        print(person)
        rating = request.POST["rating"]
        votes = request.POST["votes"]
        movie = Movies(title=title, year=year)
        person_instance = People.objects.filter(name=person)
        person_instance = person_instance[0]
        print(person_instance)
        director = Directors(movie = movie, person=person_instance)
        movie.save()
        print(movie)
        director.save()
        print(director)
        if rating and votes:
            rating_movie = Ratings(movie=movie, rating=rating, votes=votes)
            rating_movie.save()
            print (rating)
        return render(request, "peliculas/registrar_pelicula.html",{
            "mensaje": "Película guardada con éxito"
        })
    else:
        print("registrar")

        return render(request, "peliculas/registrar_pelicula.html")


# Ruta para nuevo registro de actor/director
def registrar_persona(request):
    if request.method == 'POST':
        name = request.POST["nombre"]
        year = request.POST["year"]
        person = People(name=name, birth=year)
        person.save()
        return render(request, "peliculas/registrar_persona.html",{
            "message" : "Artista registrado"
        })
        #return HttpResponseRedirect(reverse("index"))
    else:    
        return render(request, "peliculas/registrar_persona.html")


