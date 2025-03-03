function valorDesplegable(diccionario){
    var diccionarioObjeto = JSON.parse(diccionario);
    var opcion = document.getElementById("ofertaClave");
    var valor = opcion.value;
    var valores = diccionarioObjeto[valor];

    var selectSolicitudes = document.getElementById("solicitudes");
    selectSolicitudes.innerHTML = "";
    for(let i = 0; i < valores.length; i++){
        var newOption = document.createElement("option");
        newOption.value = valores[i][0];
        newOption.text = valores[i][1] + " - " + valores[i][2] + " - " + valores[i][3];
        selectSolicitudes.appendChild(newOption);
    }
}