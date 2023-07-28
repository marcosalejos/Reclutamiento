var opcionesCoordinador = [
    "Coordinador/a de Mantenimiento"
]
var opcionesSupervisor = [
    "Supervisor/a de Mantenimiento",
    "Supervisor/a de Mantenimiento Electromecánico"
]
var opcionesTecnico = [
    "Técnico/a de Mantenimiento Electromecánico - Líneas",
    "Técnico/a de Mantenimiento Electromecánico - Instalaciones",
    "Técnico/a de Desarrollo Informático",
    "Técnico/a de Mantenimiento de Instalaciones",
    "Técnico/a de Montaje y Mantenimiento Electromecánico",
    "Técnico/a de PRL (Seguridad y Salud)",
    "Técnico/a de Sistemas",
    "Técnico/a Frigorista Industrial",
    "Técnico/a de Reclutamiento y Selección"
]
var opcionesGestor = [
    "Gestor/a de Almacén"
]
var opcionesPlanner = [
    "Planner de Mantenimiento"
] 
var opcionesAdministrativo = [
    "Administrativo/a CAE",
    "Administrativo/a de Operaciones - Planta",
    "Administrativo/a Laboral y PRL",
    "Administrativo/a Contable"
] 
var opcionesAuditor = [
    "Auditor/a"
]
var opcionesController = [
    "Controller Financiero"
] 
var opcionesMontador = [
    "Montador/a"
]
var opcionesOperario = [
    "Operario/a de Fabricación"
]
var opcionesProgramador = [

    "Programador/a PLC"
]
var opcionesOtros = [
    "Otros"
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
            coordinador: opcionesCoordinador,
            supervisor: opcionesSupervisor,
            tecnico: opcionesTecnico,
            gestor: opcionesGestor,
            planner: opcionesPlanner,
            administrativo: opcionesAdministrativo,
            auditor: opcionesAuditor,
            controller: opcionesController,
            montador: opcionesMontador,
            operario: opcionesOperario,
            programador: opcionesProgramador,
            otros: opcionesOtros
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