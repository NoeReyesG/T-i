
document.addEventListener('DOMContentLoaded', function(){
   
    // Habilitar boton de busqueda cuando se ha escrito en el input 
    const inputfield = document.querySelector("#buscar");
    const search = document.querySelector('#buttonsearch');
    inputfield.addEventListener('keyup', ()=>{
        let value = inputfield.value.trim();
       
        if (value.length != 0){
            search.disabled = false;
            search.style.opacity ='1';
        }
        else{
            search.disabled = true;
            search.style.opacity = '0.5';
        }       
    })

    // Pedir confirmación antes de eliminar una película
    if (document.querySelector('#eliminarf')){
        let eliminar = document.querySelector('#eliminarf');
        eliminar.addEventListener('submit', function(e){
            e.preventDefault();
            console.log("que falla?");  
            if (confirm("¿Seguro que deseas eliminar el film?")==true){
                eliminar.submit();
            }   
        });
    }    

    // Volver los campos editables
    if (document.querySelector('.editar')){
        //seleccionamos todos los botones de editar y les damos una eventlistener
        document.querySelectorAll('.editar').forEach(editar =>{
            editar.addEventListener('click', () =>{
                let id_movie = "movie"+editar.dataset.id;
                const campos = []; 
                document.querySelectorAll(`#${id_movie} input[type=text]`).forEach(input => {
                    input.readOnly=false;
                    input.style.backgroundColor = 'white';
                    input.style.color ='black';
                })

                const form_edit_movie = document.querySelector(`#${id_movie}`);
                document.querySelector(`#${id_movie} input[type=submit]`).style.display='block';
                let id_actors = "actors"+editar.dataset.id;
                //habilitar todos los campos de los actores
                document.querySelectorAll(`#${id_actors} input[type=text]`).forEach(input => {
                    //input.readOnly=false;
                    //input.style.backgroundColor = 'white';
                    //input.style.color ='black';
                })
                //mostrar boton para eliminar actores de pelicula
                document.querySelectorAll(`#${id_actors} input[type=submit]`).forEach(input => {
                    input.style.display='inline';
                }) 

                // Mostrar la barra de busqueda para agregar actores

                const busqueda_actores = document.querySelector(`#buscar${editar.dataset.id}`);
                busqueda_actores.style.display = 'block';
                const form_buscar_actores = document.querySelector(`#form${editar.dataset.id}`)

                form_buscar_actores.addEventListener('submit', (e) => {
                    e.preventDefault();
                    nameactor = document.querySelector(`#form${editar.dataset.id} input[type=text]`).value;
                    fetch(`/buscar_actor/${nameactor}`)
                    .then(response => response.json())
                    .then(actors => {
                        actors.forEach(actor =>{
                            const element1= document.createElement('li');
                            element1.innerHTML = `
                            <form action = "#">
                            <input type="text" class="form-control" readonly="readonly" value="${actor.name}">
                            <input type="submit" class="agregaractor" onclick="" value="agregar">
                            </form>`;
                            document.querySelector(`#encontrado${editar.dataset.id}`).append(element1);
                        })
                    })
                })
                
                // event listener para actualizar datos
                form_edit_movie.addEventListener('submit', function(e){
                    e.preventDefault();
                    //volver editable los campos de director y título y guardas los valores
                    document.querySelectorAll(`#${id_movie} input[type=text]`).forEach(input => {
                        input.readOnly=true;
                        input.style.backgroundColor = '#000428';
                        input.style.color ='white';
                        campos.push(input.value);
                    })
                    // Actualizar los valores
                    fetch(`/update/${editar.dataset.id}`,{
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
    /*fetch(`/buscar/titulo`)
            .then(response => response.json())
            .then(titulos => {
                console.log(titulos);
                /*
                })
            }) */
}) 