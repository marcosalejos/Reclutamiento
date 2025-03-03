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
                horas.value = 40;
                horas.readOnly = true;
            }
            else{
                horas.value = 8;
                horas.readOnly = false;
            }
        })
    }
    const defaultPuesto = document.getElementById("puestoFirma").options[document.getElementById("puestoFirma").selectedIndex].text;
    setPuestoFirma(defaultPuesto);
});

function setPuestoFirma(defaultPuesto){
    let puestos = {
        "Ingenieria": [
            "Coordinador Ingeniería Mecánica",
            "Coordinadora Ingeniería Automatización",
            "Coordinador de Procesos, Metodología y Datos",
            "Ingeniero mecánico",
            "Ingeniero automatización",
            "Ingeniero de procesos, metodología y datos",
            "Técnico"
        ],
        "Fabricación": [
            "Coordinador Fabricación",
            "Responsable de fabricación",
            "Jefe de equipo",
            "Técnico"
        ],
        "MTEA": [
            "Direción MTEA",
            "Coordinador",
            "Supervisor Producción",
            "Planner",
            "Supervisor Instalaciones",
            "Supervisor Mantenimiento",
            "Técnico"
        ],
        "Valores y Personas":[
            "Coordinador de Valores y Personas",
            "Técnico de Valores y Personas",
            "Técnico de Prevención de Riesgos Laborales"
        ],
        "Administración y Finanzas": [
            "Coordinador de Administración y Finanzas",
            "Técnico de Administración y Finanzas"
        ],
        "Tecnologías de la Información":[
            "Coordinador de TI",
            "Ingeniero TI"
        ],
        "Comercial": ["Técnico Comercial"],
        "Compras y Aprovisionamiento": [
            "Responsable de Compras y Aprovisionamiento",
            "Técnico de Compras y Aprovisionamiento", 
            "Responsable de Almacén"
        ]
    }
    let puestoSelect = document.getElementById("puestoFirma");
    let areaSelect = document.getElementById("id_AreaFirma");
    let options = areaSelect.options;
    let index = areaSelect.selectedIndex;
    let value = options[index].text;
    puestoSelect.innerHTML = "";
    if(defaultPuesto != undefined){
        let opt = document.createElement("option");
        opt.value = defaultPuesto;
        opt.text = defaultPuesto;
        puestoSelect.append(opt);
    }
    puestos[value].forEach(puesto => {
        opt = document.createElement("option");
        opt.value = puesto;
        opt.text = puesto;
        puestoSelect.append(opt);
        opt = undefined;
    });
    
}
