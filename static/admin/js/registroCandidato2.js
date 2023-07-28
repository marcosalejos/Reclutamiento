function RellenarSolicitud(){
    var solicitudes = document.getElementById('solicitudes');
    var valor = solicitudes.options[solicitudes.selectedIndex].value;
    var texto = solicitudes.options[solicitudes.selectedIndex].text;
    console.log(texto)
    var centroIn = document.getElementById('id_Centro');
    var puestoIn = document.getElementById('id_Puesto');

    var [id, centro] = valor.split('-');
    var [solicitante, puesto, puesto2] = texto.split('-');
    console.log(puesto, puesto2)
    if(id == 34){ //El valor de la solicitud del Sistema, limpiar los campos Centro y Puesto
        centroIn.value = "";
        puestoIn.value = "";
    }else{
        centroIn.value = centro;
        if(puesto2 != null){
            puestoIn.value = puesto + " - " + puesto2;
        }else{
            puestoIn.value = puesto;
        }
    }
    var compDiv = document.getElementById('complementario');
    if(centro == 'OKOA'){
        compDiv.style.display = "flex";
    }else{
        compDiv.style.display = "none";
    }
    
}