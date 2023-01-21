from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import Movies, People, Directors, Ratings, Stars
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def index(request):
    if request.method == 'POST':
        #valido=[0,1,2]
        #for valido in valido:
        #    print(valido)
        resultado = {}
        buscarpor = request.POST["buscarpor"]
        busqueda = request.POST["buscar"]
        print(busqueda)
        if (buscarpor == '0'):
            # Hacemos la query en la base de datos, aplicamos __i exact para que sea insensitivo a mayusculas y min
            # Agregamos .strip() para eliminar espacios en blanco al principio y final
            movie = Movies.objects.filter(title__iexact=busqueda.strip())
            if movie:
                print(movie[0].id)
                movieobject = Movies.objects.get(pk=movie[0].id)
                stars = Stars.objects.filter(movie=movieobject)
                director = Directors.objects.filter(movie=movieobject)
                rating = Ratings.objects.filter(movie=movieobject)
                resultado["titulo"] = movie[0].title
                resultado["director"] = director[0].person.name
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
                "message": "Film not found",
                })
    else:
        peliculas = Movies.objects.all()

        return render(request, "peliculas/index.html",{
            "peliculas": peliculas
        })

def registrar_pelicula(request):
    return render(request, "peliculas/registrar_pelicula.html")

def registrar_persona(request):
    if request.method == 'POST':
        name = request.POST["nombre"]
        year = request.POST["year"]
        print(name)
        print(year)
        return HttpResponseRedirect(reverse("index"))
    else:    
        return render(request, "peliculas/registrar_persona.html")

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
        
