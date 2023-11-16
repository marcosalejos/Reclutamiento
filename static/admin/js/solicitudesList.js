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

function exportarAExcel() {
    /* Obtén la tabla HTML y sus datos */
    var tabla = document.getElementById('solicitudes');
    var datos = XLSX.utils.table_to_sheet(tabla);
  
    /* Crea un libro de Excel y agrega la hoja con los datos */
    var libro = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(libro, datos, 'Hoja1');
  
    /* Guarda el archivo Excel */
    XLSX.writeFile(libro, 'solicitudes.xlsx');
}
  

function FinalizadasColor(){
    let filas = document.getElementsByTagName('tr');
    for(let i = 1; i < filas.length; i++){
        let fila = filas[i].querySelectorAll('td');
        let vacantes = fila[5].innerText;
        let contratas = fila[6].innerText;
        if(filas[i].getAttribute('id') == 'Aprobada' && contratas >= vacantes){
            fila[0].style.backgroundColor = '#3dae2a';
            fila[0].style.color = 'white';

        }
    }

}

function Pendientes(){
    let pend = document.getElementById('pendBTN');
    let val = document.getElementById('valBTN');
    let fin = document.getElementById('finBTN');
    let desc = document.getElementById('descBTN');

    pend.style.opacity = 1;
    val.style.opacity = 0.3;
    fin.style.opacity = 0.3;
    desc.style.opacity = 0.3;

    let filas = document.getElementsByTagName('tr');
    for(let i = 1; i < filas.length; i++){
        let fila = filas[i];
        if(fila.getAttribute('id') == 'None'){
            fila.style.display = 'table-row';
        }else{
            fila.style.display = 'none';
        }
    }
    
}

function Validadas(){
    let pend = document.getElementById('pendBTN');
    let val = document.getElementById('valBTN');
    let fin = document.getElementById('finBTN');
    let desc = document.getElementById('descBTN');

    pend.style.opacity = 0.3;
    val.style.opacity = 1;
    fin.style.opacity = 0.3;
    desc.style.opacity = 0.3;

    let filas = document.getElementsByTagName('tr');
    for(let i = 1; i < filas.length; i++){
        let fila = filas[i].querySelectorAll('td');
        let vacantes = fila[5].innerText;
        let contratas = fila[6].innerText;
        if(filas[i].getAttribute('id') == 'Aprobada' && contratas < vacantes){
            filas[i].style.display = 'table-row';
        }else{
            filas[i].style.display = 'none';
        }
    }
}

function Finalizadas(){
    let pend = document.getElementById('pendBTN');
    let val = document.getElementById('valBTN');
    let fin = document.getElementById('finBTN');
    let desc = document.getElementById('descBTN');

    pend.style.opacity = 0.3;
    val.style.opacity = 0.3;
    fin.style.opacity = 1;
    desc.style.opacity = 0.3;

    let filas = document.getElementsByTagName('tr');
    for(let i = 1; i < filas.length; i++){
        let fila = filas[i].querySelectorAll('td');
        let vacantes = fila[5].innerText;
        let contratas = fila[6].innerText;
        if(filas[i].getAttribute('id') == 'Aprobada' && contratas >= vacantes){
            filas[i].style.display = 'table-row';
        }else{
            filas[i].style.display = 'none';
        }
    }

}

function Descartadas(){
    let pend = document.getElementById('pendBTN');
    let val = document.getElementById('valBTN');
    let fin = document.getElementById('finBTN');
    let desc = document.getElementById('descBTN');

    pend.style.opacity = 0.3;
    val.style.opacity = 0.3;
    fin.style.opacity = 0.3;
    desc.style.opacity = 1;

    let filas = document.getElementsByTagName('tr');
    for(let i = 1; i < filas.length; i++){
        let fila = filas[i];
        if(fila.getAttribute('id') == 'Denegada'){
            fila.style.display = 'table-row';
        }else{
            fila.style.display = 'none';
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
            let celdaVac = celdas[i+2];
            let vacantes = parseInt(celdaVac.innerText);
            let celdaContrata = celdas[i+3];
            let contratas = parseInt(celdaContrata.innerText);
            if(vacantes > 100){
                vacantes = 0;
                contratas = 0;
            }
            if(hashMap.has(text)){
                let valor = hashMap.get(text);
                valor += vacantes;
                valor -= contratas;
                hashMap.set(text, valor);
            }else{
                hashMap.set(text,vacantes-contratas);
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

    let pend = document.getElementById('pendBTN');
    let val = document.getElementById('valBTN');
    let fin = document.getElementById('finBTN');
    let desc = document.getElementById('descBTN');

    pend.style.opacity = 0.3;
    val.style.opacity = 0.3;
    fin.style.opacity = 0.3;
    desc.style.opacity = 0.3;

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
    FinalizadasColor();
});