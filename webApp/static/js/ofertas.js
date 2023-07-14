
window.addEventListener('DOMContentLoaded', function() {
    mostrarTabla('tabla-activas');
});
  
function mostrarTabla(tablaId) {
    var tablas = document.getElementsByClassName('styled-table');
    for (var i = 0; i < tablas.length; i++) {
      tablas[i].style.display = 'none';
    }
    var tablaMostrar = document.getElementById(tablaId);
    if (tablaMostrar) {
      tablaMostrar.style.display = 'table';
    }
}

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
            // si no ha encontrado ninguna coincidencia, esconde la
            // fila de la tabla
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

function Search(){
    var tablaActivas = document.getElementById("tabla-activas")
    var tablaInactivas = document.getElementById("tabla-inactivas")
    if(tablaActivas.style.display == 'table'){
      SearchTable(tablaActivas)
    }
    else if (tablaInactivas.style.display == 'table'){
      SearchTable(tablaInactivas)
    }
}