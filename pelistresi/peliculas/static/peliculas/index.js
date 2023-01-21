
document.addEventListener('DOMContentLoaded', function(){
    const selectpor = document.querySelector('#buscarpor');
    const labelbuscar = document.querySelector('#buscarl');
    const inputfield = document.querySelector("#buscar");

    /*fetch(`/buscar/titulo`)
            .then(response => response.json())
            .then(titulos => {
                console.log(titulos);
                /*
                inputfield.addEventListener('keyup', ()=>{
                    titulos.forEach(titulo =>{ 
                     if (titulo.toLowerCase().startsWith(inputfield.ariaValueMax.toLocaleLowerCase()) && inputfield.value !=""){
                        let listitem = document.createElement("li");
                        listitem.classList.add("list-items");
                        listitem.style.cursor = "pointer";

                     }   
                    })
                })
            }) */
    /*Cambiamos la etiqueta del campo de busqueda de acuerdo a si se seleccionó 
    busqueda por película, actor o director*/
    selectpor.addEventListener('change', function(){
        if (selectpor.value == '0'){
            labelbuscar.innerHTML = "Ingresa el título";
            
        }
        if (selectpor.value == '1'){
            labelbuscar.innerHTML = "Ingresa el nombre de la actriz/actor";
           /* fetch(`/buscar/titulo`)
            .then(response => response.json())
            .then(titulos => {
                titulos.forEach(titulo =>{ 
                console.log(titulo);
                })
            })*/
        }
        if (selectpor.value == '2'){
            labelbuscar.innerHTML = "Ingresa el nombre del director(a)";
        }
    })
    

})