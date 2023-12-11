const formAprobar = document.getElementById("formAprobar");
const hdnID = document.getElementById("id_planilla");
const botones = document.querySelectorAll(".btn-success");

for (const boton of botones) {
    boton.addEventListener("click", e => {
        e.preventDefault();
        hdnID.value = boton.id;
        formAprobar.submit();
    });
}

alert("dash carga");