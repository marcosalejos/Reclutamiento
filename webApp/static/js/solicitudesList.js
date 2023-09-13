function SearchTable(table){
    const searchText = document.getElementById('search').value.toLowerCase();
    let total = 0;
    // Recorremos todas las filas con contenido de la tabla
    for (let i = 1; i < table.rows.length; i++) {
        // Si el td tiene la clase "noSearch" no se busca en su cntenido
        if (table.rows[i].classList.contains("noSearch")) {
            continue;
        }
        let found = false;
        const cellsOfRow = table.rows[i].getElementsByTagName('td');
        // Recorremos todas las celdas
        for (let j = 0; j < cellsOfRow.length && !found; j++) {
            const compareWith = cellsOfRow[j].innerHTML.toLowerCase();
            // Buscamos el texto en el contenido de la celda
            if (searchText.length == 0 || compareWith.indexOf(searchText) > -1) {
                found = true;
                total++;
            }
        }
        if (found) {
        table.rows[i].style.display = '';
        } else {
            // si no ha encontrado ninguna coincidencia, esconde la fila de la tabla
            table.rows[i].style.display = 'none';
        }
    }
    // mostramos las coincidencias
    const lastTR=table.rows[table.rows.length-1];
    const td=lastTR.querySelector("td");
    lastTR.classList.remove("hide", "red");
    if (searchText == "") {
        lastTR.classList.add("hide");
    }

}

function HiddeDelete(){
    let contratadosList = document.getElementsByName("contratados");
    let deleteButtons = document.getElementsByName("delete");
    for(let i = 0; i < contratadosList.length; i++){
        let valor = contratadosList[i].innerText;
        if(valor > 0){
            deleteButtons[i].style.display = "none";
        }
    }
}

function MostrarFilasValidadas(estado){
    var filas = document.getElementsByTagName("tr");
    var filasEstado = [];
    for(let i = 1; i < filas.length; i++){
        filas[i].style.display = 'none';
        if(filas[i].getAttribute('id') === estado){
            filasEstado.push(filas[i]);
        }
    }
    for(let i = 0; i < filasEstado.length; i++){
        filasEstado[i].style.display = "table-row";
    }
}

function FiltroContratacion(estado){
    var filas = document.getElementsByTagName("tr");
    if(estado == "Abierta"){
        for(let i = 1; i < filas.length; i++){
            let contrataList = document.getElementsByName("contratados");
            let contrata = contrataList[i-1];
            let contrataText = contrata.innerText;
            let vacantesList = document.getElementsByName("vacantes");
            let vacantes = vacantesList[i-1];
            let vacantesText = vacantes.innerText;
            if(contrataText < vacantesText){
                filas[i].style.display = "table-row";
            }else{
                filas[i].style.display = "none";
            }
        }
    }else if(estado == "Cerrada"){
        for(let i = 1; i < filas.length; i++){
            let contrataList = document.getElementsByName("contratados");
            let contrata = contrataList[i-1];
            let contrataText = contrata.innerText;
            let vacantesList = document.getElementsByName("vacantes");
            let vacantes = vacantesList[i-1];
            let vacantesText = vacantes.innerText;
            if(contrataText == vacantesText){
                filas[i].style.display = "table-row";
            }else{
                filas[i].style.display = "none";
            }
        }
    }
}

function FiltroValidacion(){
    var checkbox = document.getElementById("checkValidaciones");
    var filas = document.getElementsByTagName("tr");
    var filasValidadas = [];
    var filasNoVal = [];
    var aprLink = document.getElementById("aprobadas");
    var denLink = document.getElementById("denegadas");
    for(let i = 1; i < filas.length; i++){
        let fila = filas[i];
        if(fila.getAttribute('id') === 'None'){
            filasNoVal.push(fila);
        }else{
            filasValidadas.push(fila);
        }
    }
    if(checkbox.checked){
        aprLink.style.display = "none";
        denLink.style.display = "none";
        for(let i = 0; i < filasValidadas.length; i++){
            filasValidadas[i].style.display = "none";
        }
        for(let i = 0; i < filasNoVal.length; i++){
            filasNoVal[i].style.display = "table-row";
        }
    }else{
        aprLink.style.display = "flex";
        denLink.style.display = "flex";
        for(let i = 0; i < filasNoVal.length; i++){
            filasNoVal[i].style.display = "none";
        }
        for(let i = 0; i < filasValidadas.length; i++){
            filasValidadas[i].style.display = "table-row";
        }
    }  
}

function SolicitudesCount(){
    let hashMap = new Map();
    let celdas = document.getElementsByTagName('td');
    for(let i = 0; i < celdas.length; i++){
        let centro = celdas[i];
        if(centro.getAttribute('id') === 'centro'){
            let text = centro.innerText;
            if(hashMap.has(text)){
                let valor = hashMap.get(text);
                hashMap.set(text, ++valor);
            }else{
                hashMap.set(text,1);
            }
        }
    }
    Resumen(hashMap);
}

function Resumen(hashMap){
    let enc = document.getElementById('encabezados');
    let valores = document.getElementById('valores');
    var suma = 0;

    hashMap.forEach((valor,clave) => {
        let divEncabezado = document.createElement('div');
        divEncabezado.classList.add('enc');
        enc.appendChild(divEncabezado);
        let encabezadoLink = document.createElement('a');
        encabezadoLink.innerHTML = clave;
        encabezadoLink.onclick = () => FiltrarTabla(clave);
        divEncabezado.appendChild(encabezadoLink);
        let divValor = document.createElement('div');
        divValor.innerText = valor;
        divValor.classList.add('enc');
        valores.appendChild(divValor);

        suma += valor;
    });

    let encabezadoTot = document.createElement('div');
    encabezadoTot.classList.add('enc_tot');
    enc.appendChild(encabezadoTot);
    let linkTot = document.createElement('a');
    linkTot.innerHTML = "TOTAL";
    linkTot.onclick = () => FiltrarTabla('total');
    encabezadoTot.appendChild(linkTot);

    let valorTot = document.createElement('div');
    valorTot.innerText = suma;
    valorTot.classList.add("enc_tot");
    valores.appendChild(valorTot);

}

function FiltrarTabla(centro){
    let filas = document.getElementsByTagName('tr');
    if(centro === 'total'){
        for (let i = 0; i < filas.length; i++) {
            filas[i].style.display = 'table-row';
          }
    }else{
        for (let i = 1; i < filas.length; i++) {
            filas[i].style.display = 'none';
          }
        
          for (let i = 0; i < filas.length; i++) {
            let celdas = filas[i].querySelectorAll('td');
            for (let j = 0; j < celdas.length; j++) {
              if (celdas[j].innerText === centro) {
                filas[i].style.display = 'table-row';
                break;
              }
            }
          }
    }
}
window.addEventListener('DOMContentLoaded', function() {
    SolicitudesCount();
    HiddeDelete();
    FiltroValidacion();
});