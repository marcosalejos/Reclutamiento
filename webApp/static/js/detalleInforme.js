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
    console.log(res);
    iban.value = res;
}