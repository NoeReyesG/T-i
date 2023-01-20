from django.db import models

# Create your models here.

# Estamos creando una abstracción de una base de datos para peliculas.
# Los modelos en Django pueden administrar diferentes BD, para el problema solicitado SQLite es suficiente, pero con algo de 
# configuración, podemos conectar si fuera necesario a alguna otra cómo MySQL, por ejemplo.

# Modelo equivalente a una tabla para peliculas 
class Movies(models.Model):
    title = models.CharField( max_length=300, default=None)
    year = models.IntegerField( default=None)

# Modelo equivalente a una tabla para las personas
class People(models.Model):
    name = models.CharField(max_length = 400)
    birth = models.IntegerField(blank=True)

# Modelo equivalente a una tabla que conecta a las personas con las peliculas en las que actúan o participan.
class Stars(models.Model):
    movie_id = models.ForeignKey(Movies, on_delete=models.CASCADE, default=None)
    person_id = models.ForeignKey(People, on_delete=models.CASCADE, default=None)

#Modelo equivalente a una tabla que conecta a los directores con las peliculas que dirijieron
class Directors(models.Model):
    movie_id = models.ForeignKey(Movies, on_delete=models.CASCADE, default=None)
    person_id = models.ForeignKey(People, on_delete=models.CASCADE, default=None)

class Ratings(models.Model):
    movie_id = models.ForeignKey(Movies, on_delete=models.CASCADE, default=None)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    votes = models.IntegerField()

