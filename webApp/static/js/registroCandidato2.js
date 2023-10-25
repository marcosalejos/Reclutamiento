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
    if(id == 38){ //El valor de la solicitud del Sistema, limpiar los campos Centro y Puesto
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

document.addEventListener('DOMContentLoaded', function(){
    const jornadaSelect = document.getElementById("id_Jornada");
    var horas = document.getElementById("id_Horas");
    if(jornadaSelect.value == "Completa"){
        horas.readOnly = true;
    }
    if(jornadaSelect){
        jornadaSelect.addEventListener("change", function(){
            let jornadaValue = jornadaSelect.value;
            if(jornadaValue == "Completa"){
                horas.value = 8;
                horas.readOnly = true;
            }
            else{
                horas.value = 6;
                horas.readOnly = false;
            }
        })
    }
});