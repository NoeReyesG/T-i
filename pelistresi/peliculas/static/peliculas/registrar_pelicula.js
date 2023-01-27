// Esperamos a que el documento cargue
document.addEventListener('DOMContentLoaded', function(){
    // Agregamos un event listener para cuando se envie el formulario checar si el director existe en la BD.
    document.querySelector('#registrar-film').addEventListener('submit', (e)=>{
        e.preventDefault();
        director = document.querySelector('#director').value;
        console.log(director);
        fetch(`/buscar_persona/director/${nameactor}`)
        .then(response => response.json())
        .then(resultado => {
            if (resultado.resultado == "no encontrado"){
                document.querySelector('#mensaje').style.display = 'block';
            }
            if (resultado.resultado == "encontrado"){
                e.submit();
            }     
        })
    })
})