var opcionesMTEA = [
    "Coordinador (Plantas)",
    "Planner (Planta)",
    "Supervisor Mantenimiento (Plantas)",
    "Supervisor Producción (Plantas)",
    "Supervisor Instalaciones (Plantas)",
    "Técnico de Mantenimiento Electromecánico",
    "Técnico de Montaje y Mantenimiento Electromecánico",
    "Técnico de Instalaciones",
    "Gestor de Compras / Almacén"
]
var opcionesMet = [
    "Coordinador Procesos, Metodología y Datos",
    "Ingeniero Procesos, Metodología y Datos"
]
var opcionesIngMec = [
    "Coordinador Ingeniería Mecánica",
    "Ingeniero Mecánico",
    "Delineante"
]
var opcionesIngAut = [
    "Coordinador Ingeniería Automatización",
    "Jefe de Equipo Automatización",
    "Programador de PLC y Robótica"
]
var opcionesFabMec = [
    "Coordinador Fabricación Mecánica",
    "Supervisor de Taller",
    "Jefe de Equipo - Montaje Mecánico",
    "Técnico de Montaje Mecánico",
    "Técnico Granalladora"
] 
var opcionesIngEl = [
    "Ingeniero Eléctrico"
] 
var opcionesFabEl = [
    "Técnico de Montaje Electromecánico"
]
var opcionesAdmin = [
    "Coordinador de Administración y Finanzas",
    "Técnico de Administración y Finanzas"
] 
var opcionesTI = [
    "Coordinador de TI",
    "Ingeniero de TI"
]
var opcionesComercial = [
    "Técnico Comercial "
]
var opcionesCompras = [
    "Técnico de Compras y Aprovisionamiento ",
    "Gestor de Almacén"
]
var opcionesVYP = [
    "Coordinador de Valores y Personas",
    "Técnico de Valores y Personas"
]

var opcionesPRL = [
    "Coordinador de PRL",
    "Técnico de PRL" 
]

function opcionesDesplegable(){
    var selectSecundario = document.getElementById("opciones");
    var selectPrimario = document.getElementById('puestos');
    var opcionSeleccionada = selectPrimario.options[selectPrimario.selectedIndex];
    var optionValue = opcionSeleccionada.value;
    var optionText = opcionSeleccionada.text;

    selectSecundario.innerHTML = "";

    if (optionValue !== "") {
        const opciones = {
            MTEA: opcionesMTEA,
            Metodologia: opcionesMet,
            Ing_Mec: opcionesIngMec,
            Ing_Aut: opcionesIngAut,
            Fab_Mec: opcionesFabMec,
            Ing_Elec: opcionesIngEl,
            Fab_Elec: opcionesFabEl,
            Administracion: opcionesAdmin,
            TI: opcionesTI,
            Comercial: opcionesComercial,
            Compras: opcionesCompras,
            VyP: opcionesVYP,
            PRL: opcionesPRL
        };

        const selectedOpciones = opciones[optionValue];

        for (let i = 0; i < selectedOpciones.length; i++) {
            let newOption = document.createElement("option");
            newOption.value = selectedOpciones[i];
            newOption.text = selectedOpciones[i];
            selectSecundario.appendChild(newOption);
        }
    }

}

window.addEventListener('DOMContentLoaded', function() {
    opcionesDesplegable();
});