
document.addEventListener('DOMContentLoaded', function(){
   
    /* Habilitar boton de busqueda cuando se ha escrito en el input */
    // buscamos el campo de texto  
    const inputfield = document.querySelector("#buscar");
    // buscamos el boton de busqueda
    const search = document.querySelector('#buttonsearch');
    // agregamos un evento para cada de que se presiona una tecla en el campo de texto
    inputfield.addEventListener('keyup', ()=>{
        // obtenemos el valor del campo de texto y le quitamos los espacios al final y al principio
        let value = inputfield.value.trim();
       //Si hay algo escrito en el campo de texto habilitamos el botón de busqueda, en caso contrario lo deshabilitamos
        if (value.length != 0){
            search.disabled = false;
            search.style.opacity ='1';
        }
        else{
            search.disabled = true;
            search.style.opacity = '0.5';
        }       
    })

    /* Pedir confirmación antes de eliminar una película*/
    // Verificamos que haya un formulario para eliminar, el cual se despliega solo si se ha hecho
    // una busqueda exitosa y se desplegó información de una película
    if (document.querySelector('.eliminarf')){
        // Obtenemos el formulario y le damos un event listener para el momento de enviar el formulario
        document.querySelectorAll('.eliminarf').forEach( eliminar =>{
        eliminar.addEventListener('submit', function(e){
            //evitamos que la forma se envíe, pedimos confirmación al usuario, en caso de ser positiva, enviamos el formulario
            e.preventDefault();  
            if (confirm("¿Seguro que deseas eliminar el film?")==true){
                eliminar.submit();
            }   
        })
        })
    }
    

    /* Editar el contenido */
    if (document.querySelector('.editar')){
        // Seleccionamos todos los botones de editar y les damos una eventlistener 
        document.querySelectorAll('.editar').forEach(editar =>{
            editar.addEventListener('click', () =>{
                // Obtenemos el id de cada boton editar, id que hemos previsto para que sea un identificador único
                // utilizando el id de la pelicula
                let id_movie = editar.dataset.id;
                //Ocultamos el boton editar
                editar.style.display='none';
                const campos = []; 
                // Seleccionamos los campos tipo texto asociados los cuales corresponden al titulo de la pelicula y el director 
                document.querySelectorAll(`#movie${id_movie} input[type=text]`).forEach(input => {
                    // Volvemos los campos editables
                    input.readOnly=false;
                    input.style.backgroundColor = 'white';
                    input.style.color ='black';
                })
                // Obtenemos la forma ppara editar los campos titulo y director de una película en especifico
                const form_edit_movie = document.querySelector(`#movie${id_movie}`);
                document.querySelector(`#movie${id_movie} input[type=submit]`).style.display='block';
                let id_actors = "actors"+id_movie;
                //habilitar todos los campos de los actores
                document.querySelectorAll(`#${id_actors} input[type=text]`).forEach(input => {
                    let form = input.parentElement.parentElement;
                    form.addEventListener('submit', (e)=>{
                        e.preventDefault
                        fetch(`/eliminar_star/${input.dataset.id}/${id_movie}`,{method: 'PUT'}) 
                        form.remove()
                    })
                
                    //input.readOnly=false;
                    //input.style.backgroundColor = 'white';
                    //input.style.color ='black';
                })
                //mostramos el area para busqueda de actores para agregarlos a la pelicula
                document.querySelector(`#encontrado${id_movie}`).style.display='block';    
                // Mostramos los botones para eliminar actores de pelicula
                document.querySelectorAll(`#${id_actors} input[type=submit]`).forEach(input => {
                    input.style.display='block';
                }) 

                // Mostrar la barra de busqueda para agregar actores
                const busqueda_actores = document.querySelector(`#buscar${id_movie}`);
                busqueda_actores.style.display = 'block';
                // Obtenemos el formulario para la busqueda de actores para agregarlos a un film
                const form_buscar_actores = document.querySelector(`#form${id_movie}`)

                // Agregamos un evento al formulario de buscar actores y prevenimos el submit
                form_buscar_actores.addEventListener('submit', (e) => {
                    e.preventDefault();
                    // Obtenemos el nombre del actor escrito en el campo de texto de busqueda
                    nameactor = document.querySelector(`#form${id_movie} input[type=text]`).value;
                    // Hacemos la busqueda, en caso de ser exitosa se desplegara el resultado,
                    // el cual puede ser hasta de tres actores si hay multiples coincidencias en el substring 
                    fetch(`/buscar_actor/${nameactor}`)
                    .then(response => response.json())
                    .then(actors => {
                        actors.forEach(actor =>{
                            const element0 = document.createElement('li');
                            const element1= document.createElement('form');
                            element1.setAttribute("action", "#");
                            element1.innerHTML = `
                            <input type="text" class="form-control" readonly="readonly" value="${actor.name}">
                            <input type="submit" class="agregaractor" value="agregar">
                            `;
                            element1.addEventListener('submit', function(e){
                                e.preventDefault();
                                console.log("prevent")
                                fetch(`/agregar_actor/${id_movie}`,{
                                    method: 'PUT',
                                    body: JSON.stringify({
                                    person:actor.name
                                    })   
                                })
                                element1.innerHTML=`<h4>Agregado</h4>`
                                //.then(response => response.json())
                                //.then(actors => {
                            })
                            element0.appendChild(element1);
                            document.querySelector(`#encontrado${id_movie}`).append(element0);
                        })
                    })
                })
                
                /* event listener para actualizar datos titulo y director */
                form_edit_movie.addEventListener('submit', function(e){
                    e.preventDefault();
                    //volver no editable los campos de director y título y guardas los valores
                    document.querySelectorAll(`#movie${id_movie} input[type=text]`).forEach(input => {
                        input.readOnly=true;
                        input.style.backgroundColor = '#000428';
                        input.style.color ='white';
                        campos.push(input.value);
                        // Ocultar boton guardar cambios
                        document.querySelector(`#movie${id_movie} input[type=submit]`).style.display='none';
                        // Ocultar busqueda de actores
                        busqueda_actores.style.display = 'none';
                        //Ocultar botones de eliminar
                        document.querySelectorAll(`#${id_actors} input[type=submit]`).forEach(input => {
                            input.style.display='none';
                        // Ocultar los resultados de busqueda de actores si existe
                        if(document.querySelector(`#encontrado${id_movie}`)){
                            document.querySelector(`#encontrado${id_movie}`).style.display='none';
                        }
                        // mostrar boton editar nuevamente
                        editar.style.display='block';
                        })
                    })
                    // Actualizar los valores utilizando method put
                    fetch(`/update/${id_movie}`,{
                        method: 'PUT',
                        body: JSON.stringify({
                            title:campos[0],
                            director: campos[1]
                        })   
                    })//end fetch
            
                }) //end edit eventlistener
            })
        })    
    }

    /* Diseño responsive */
    window.addEventListener('resize', function() {
        const win = window.innerWidth;
        const formulario = document.querySelector('#busqueda')
        const boton_buscar = document.querySelector('#busqueda div input[type=submit]');
        if (win < 768) {
          document.querySelectorAll('#busqueda div').forEach(div => {
                div.classList.remove('col-auto');
          })

          formulario.classList.remove('row');
          formulario.classList.remove('g-3');
          formulario.classList.add('container2');
          document.querySelector('#busqueda div label').classList.add('form-label');
          boton_buscar.parentElement.style.display='flex';
          boton_buscar.parentElement.style.justifyContent ='flex-end';
        } 

        else {
          document.querySelectorAll('#busqueda div').forEach(div => {
            div.classList.add('col-auto');
            })
          formulario.classList.add('row');
          formulario.classList.add('g-3');
          formulario.classList.remove('container2');
        }
      });
}) 