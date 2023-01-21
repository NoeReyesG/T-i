from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Movies, People, Directors, Ratings, Stars
# Create your views here.

def index(request):
    
    return render(request, "peliculas/index.html")

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
