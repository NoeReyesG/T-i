# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

# Modelo que equivale a tabla de peliculas 
class Movies(models.Model):
    title = models.TextField()
    year = models.IntegerField(blank=True, null=True) 

    def serialize(self):
        return{ "titulo": self.title }
    
class People(models.Model):
    name = models.TextField()
    birth = models.IntegerField(blank=True, null=True) 
    

class Directors(models.Model):
    movie = models.ForeignKey('Movies', on_delete=models.CASCADE, default=None)
    person = models.ForeignKey('People', on_delete=models.CASCADE, default=None)

    def serialize(self):
        return{ "director": self.person.name }

class Ratings(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, default=None)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    votes = models.IntegerField()


class Stars(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, default=None)
    person = models.ForeignKey(People, on_delete=models.CASCADE, default=None)

    def serialize(self):
        return{ "actor": self.person.name }

