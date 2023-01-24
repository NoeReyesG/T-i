from django.db import models

# Modelo que equivale a tabla de peliculas 
class Movies(models.Model):
    title = models.TextField()
    year = models.IntegerField(blank=True, null=True) 

    def serialize(self):
        return{ "titulo": self.title }
 # Modelo que equivale a una tabla de Personas   
class People(models.Model):
    name = models.TextField()
    birth = models.IntegerField(blank=True, null=True)
    
    def serialize(self):
        return{
                "id":self.id,
                "name": self.name 
                }    
# Modelo que equivale a una relacion many to many de personas y peliculas para registrar directores
class Directors(models.Model):
    movie = models.ForeignKey('Movies', on_delete=models.CASCADE, default=None)
    person = models.ForeignKey('People', on_delete=models.CASCADE, default=None)

    def serialize(self):
        return{ "director": self.person.name }

# modelo que equivale a una tabla de ratings
class Ratings(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, default=None)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    votes = models.IntegerField()

# Modelo que equivale a una relacion many to many de personas y peliculas para registrar actores
class Stars(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, default=None)
    person = models.ForeignKey(People, on_delete=models.CASCADE, default=None)
    def serialize(self):
        return {
            "id": self.person.id,
            "name": self.person.name,
            "birth": self.person.birth
        } 

    
