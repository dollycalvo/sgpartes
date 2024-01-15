const formAbrirPlanilla = document.querySelector("#formAbrirPlanilla");
const hdnIdPlanilla = document.getElementById("hdnIdPlanilla");
const bloquesPlanillas = document.querySelectorAll(".bloque-revision-planilla");

bloquesPlanillas.forEach(bloque => {
    bloque.addEventListener("click", event => {
        event.preventDefault();
        hdnIdPlanilla.value = bloque.id;
        formAbrirPlanilla.submit();
    });
});
