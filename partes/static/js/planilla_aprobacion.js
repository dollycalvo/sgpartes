const formAprobar = document.querySelector("#formAprobar");
const btnAprobar = document.getElementById("btnAprobar");
const btnRevisar = document.getElementById("btnRevisar");
const hdnAprobar = document.getElementById("hdnAprobar");
const txtObservaciones = document.getElementById("txtObservaciones");

btnAprobar.addEventListener("click", event => {
    event.preventDefault();
    if (confirm("¿Confirma que desea aprobar la presente planilla?")) {
        hdnAprobar.value = 1;
        formAprobar.submit();
    }
});

btnRevisar.addEventListener("click", event => {
    event.preventDefault();
    if (txtObservaciones.value.trim() === "") {
        alert("Por favor, ingrese sus observaciones para notificar al agente.");
        return;
    }
    if (confirm("¿Confirma que desea enviar a revisión la presente planilla?")) {
        hdnAprobar.value = 0;
        formAprobar.submit();
    }
});
