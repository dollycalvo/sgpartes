const formAprobar = document.querySelector("#formAprobar");
const btnAprobar = document.getElementById("btnAprobar");

btnAprobar.addEventListener("click", event => {
    event.preventDefault();
    if (confirm("¿Confirma que desea aprobar la presente planilla?")) {
        formAprobar.submit();
    }
});
