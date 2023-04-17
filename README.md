# Tresi
## Ejercicio en proceso de reclutamiento como practicante para Triple i soluciones

### Desarrollo una aplicación web usando Python.
* muestra un listado de peliculas. 
* El usuario puede editar información sobre la película, ver el detalle de la película (los datos como titulo, director, actores, etc..) y puede borrar peliculas.

Se puede consultar la aplicación deployada en Azure [AQUI](https://triplei-peliculas.azurewebsites.net/) (En ocasiones tarda unos minutos en cargar ya que está alojada con una cuenta gratuita)

La aplicación se creó usando Python, en especifico el framework Django, JavaScript, HTML, CSS y algunas clases de bootstrap.

Se creó una base de datos y se hizo la inserción de las películas estrenadas en 2022. Se conectó con SQLite para administrar la BD, pero de ser necesario se puede configurar para que se administre en MySQL o alguna otra, para este ejercicio no me pareciió necesario.

La página soporta busqueda con multiples resultados, muestra hasta 5 coincidencias, no permite que se agregue más de una vez un mismo actor a una pelicula, entre otras características.  

Se creó un proyecto Django y se realizaron las configuraciones iniciales. Los archivos que me parece son de interes estan en **tresi/tresi/pelistresi/peliculas**  en dónde se encuentra:

* **models.py** el cuál incluye los modelos. Es la creación de una base de datos a través de clases que equivalen a tablas.
* **views.py** incluye el código python que administra las rutas creadas en *urls.py.*  Es el código python del back end.
* En **templates/peliculas** se encuentran los archivos .html, **index.html** es el principal, se puede notar el código embebido.
* En **static/peliculas** se encuentran los archivos styles.css, el archivo **index.js** y el archivo registrar_pelicula.js que contienen el JavaScript utilizado. El index.js contiene practicamente todo el javaScript.

Para correr el proyecto es necesario instalar los especificado en el archivo requirements.txt. Desde la carpeta *tresi/tresi/pelistresi* se ejecuta el comando **python manage.py runserver**






