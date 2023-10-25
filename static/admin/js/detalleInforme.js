window.addEventListener('DOMContentLoaded', function() {
    FormatIBAN();
});

function FormatIBAN(){
    var iban = document.getElementById('iban');
    var valor = iban.value;
    val1 = valor.substring(0,4);
    val2 = valor.substring(4,8);
    val3 = valor.substring(8,12);
    val4 = valor.substring(12,14);
    val5 = valor.substring(14);
    var res = val1 + "-" + val2 + "-" + val3 +  "-" + val4 + "-" + val5;
    iban.value = res;
}



document.addEventListener('DOMContentLoaded', function(){
    const fileInputDNI = document.getElementById('id_DNI');
    const outDNI = document.getElementById('fileDNI');
    fileInputDNI.addEventListener('change', function(){
        if(fileInputDNI.files.length > 0){
            const fileName = fileInputDNI.files[0].name;
            outDNI.textContent = fileName;
        }else{
            outDNI.textContent = 'Ningún archivo seleccionado';
        }
    });

    const fileInputSIP = document.getElementById('id_SIP');
    const outSIP = document.getElementById('fileSIP');
    fileInputSIP.addEventListener('change', function(){
        if(fileInputSIP.files.length > 0){
            const fileName = fileInputSIP.files[0].name;
            outSIP.textContent = fileName;
        }else{
            outSIP.textContent = 'Ningún archivo seleccionado';
        }
    });

    const fileInputTit = document.getElementById('id_Titularidad');
    const outTit = document.getElementById('fileTit');
    fileInputTit.addEventListener('change', function(){
        if(fileInputTit.files.length > 0){
            const fileName = fileInputTit.files[0].name;
            outTit.textContent = fileName;
        }else{
            outTit.textContent = 'Ningún archivo seleccionado';
        }
    });
})




