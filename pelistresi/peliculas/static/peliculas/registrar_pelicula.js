// Esperamos a que el documento cargue
document.addEventListener('DOMContentLoaded', function(){
    // Agregamos un event listener para cuando se envie el formulario checar si el director existe en la BD.
    const forma_agregar_film  = document.querySelector('#registrar-film')
    
    forma_agregar_film.addEventListener('submit', (e)=>{
        e.preventDefault();
        console.log(director);
        director = document.querySelector('#director').value.trim();
        console.log("noe"+director);
        if (director != ""){
            fetch(`/buscar_persona/director/${director}`)
            .then(response => response.json())
            .then(resultado => {
                if (resultado.resultado == "no encontrado"){
                    document.querySelector('#mensaje').style.display = 'block';
                }
                if (resultado.resultado == "encontrado"){
                    forma_agregar_film.submit();
                }    
            
            })
        }    
    })
               
})