# Tresi
## Ejercicio en proceso de reclutamiento para Tres i

### Desarrollo una aplicación web usando Python.
* muestra un listado de peliculas. 
* El usuario puede editar información sobre la película, ver el detalle de la película (los datos como titulo, año, género, actores, etc..) y puede borrar peliculas.

La aplicación se creó usando Python, en especifico el framework Django JavaScript HTML, CSS y algunas clases de bootstrap

Se creó una base de datos y se hizo la inserción de las películas estrenadas en 2022. Se conectó con SQLite para administrar la BD, pero de ser necesario se puede configurar para que se administre en MySQL, para este ejercicio no me pareciió necesario.

Se creó un proyecto Django y se realizaron las configuraciones iniciales, no entraré en detalles de esto ya que no es el fin. Los archivos que me parece son de interes estan en **tresi/tresi/pelistresi/peliculas**  en dónde se encuentra:

* **models.py** el cuál incluye los modelos, es la creación de una base de datos a través de clases que equivalen a tablas.
* **views.py** incluye el codigo python que administra las rutas creadas en *urls.py* es el codigo python del back end.
* En **templates/peliculas** se encuentran los archivos .html, **index.html** es el principal, se puede notar el código embebido.
* En **static/peliculas** se encuentran los archivos styles.css y el archivo **index.js** que contiene el JavaScript utilizado en index.html el cual contiene practicamente toda la aplicación.

Para correr el proyecto, desde la carpeta *tresi/tresi/pelistresi* se ejecuta el comando <span style="color:red">python manage.py runserver</span>

**nota final** *Por ahora envío lo que he programado del ejercicio solicitado, porque no quiero llegar tarde a sus consideraciones, pero aún resta mucho trabajo por hacer para considerar la aplicación aceptable. Las rutas fuera de index no están completas, hay muchas areas de mejora, me falta trabajar en el diseño responsive y agregar animaciones para una mejor experiencia de usuario, y completar comentarios por ejemplo, sin embargo creo que con lo que se cuenta hasta ahora se puede ver si sería alguien con las caracteristicas que requieren*





