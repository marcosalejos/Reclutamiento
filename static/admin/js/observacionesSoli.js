function EditObs(observacionID){
    var textarea = document.getElementById('T'+observacionID);
    var text = document.getElementById('P'+observacionID);
    var delBtn = document.getElementById('D'+observacionID);
    var okBtn = document.getElementById('A'+observacionID);
    text.style.display = 'none';
    textarea.style.display = 'flex';
    delBtn.style.display = 'none';
    okBtn.style.display = 'flex';
}

function Cancel(observacionID){
    var textarea = document.getElementById('T'+observacionID);
    var text = document.getElementById('P'+observacionID);
    var p = text.querySelector('p');
    var ta = textarea.querySelector('textarea');
    ta.value = p.textContent; //Resetear el valor del textaera en caso de cancelarlo

    var delBtn = document.getElementById('D'+observacionID);
    var okBtn = document.getElementById('A'+observacionID);

    text.style.display = 'flex';
    textarea.style.display = 'none';
    delBtn.style.display = 'flex';
    okBtn.style.display = 'none';

}

function Save(observacionID, solicitudID){
    var textarea = document.getElementById('T'+observacionID);
    var ta = textarea.querySelector('textarea');
    var descripcion = ta.value;
    console.log(descripcion);
    var url = "https://192.168.2.252/updateObservacion/" + observacionID + "/" + descripcion + "/" + solicitudID;
    window.location.href = url;
}