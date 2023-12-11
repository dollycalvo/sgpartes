const formPlanilla = document.querySelector("#formPlanilla");
const btnLimpiarForm = document.querySelector("#btnLimpiarForm");
const btnGuardarCambios = document.querySelector("#btnGuardarCambios");
const btnPresentarPlanilla = document.querySelector("#btnPresentarPlanilla");
const hdnAccionSubmit = document.querySelector("#hdnAccionSubmit");
const opcionesAccionesSubmit = hdnAccionSubmit.getAttribute("opciones").split("#");
const noFilesSelectedText = document.getElementById("noFilesSelectedText");
const areaAdjunto = document.getElementById("area-adjunto");
const pdfInput = document.getElementById("pdf");
const SIN_NOVEDAD = "Sin novedad";
const S_N = "sn";

btnLimpiarForm.addEventListener("click", () => {
    const inputs = document.querySelectorAll("input.input-registro-diario");
    inputs.forEach(input => input.value = SIN_NOVEDAD);
    const selects = document.querySelectorAll("select.input-registro-diario");
    selects.forEach(sel => sel.value = S_N);
});

btnGuardarCambios.addEventListener("click", event => {
    event.preventDefault();
    hdnAccionSubmit.value = opcionesAccionesSubmit[0];
    formPlanilla.submit();
});

btnPresentarPlanilla.addEventListener("click", () => {
    if (confirm("¿Confirma que desea presentar la planilla?\nUna vez presentada, los datos se enviarán a su supervisor y no podrá ser modificada.")) {
        hdnAccionSubmit.value = opcionesAccionesSubmit[1];
        formPlanilla.submit();
    }
});

noFilesSelectedText.addEventListener("dragover", event => {
    event.preventDefault();
    noFilesSelectedText.classList.add("file-drag-over");
});

noFilesSelectedText.addEventListener("dragleave", event => {
    event.preventDefault();
    noFilesSelectedText.classList.remove("file-drag-over");
});

noFilesSelectedText.addEventListener("drop", event => {
    console.log(event);
    event.preventDefault();
    noFilesSelectedText.classList.remove("file-drag-over");
    archivoAdjuntado(event.dataTransfer.files[0].name);
});

function fileInputOpen() {
    pdfInput.click();
}

function archivoAdjuntado(nombre) {
    const wrapperNombreArchivo = document.getElementById("wrapperNombreArchivo");
    const nombreArchivo = document.getElementById("nombreArchivo");
    nombreArchivo.innerHTML = nombre;
    wrapperNombreArchivo.classList.remove("d-none");
    noFilesSelectedText.classList.add("d-none");
    areaAdjunto.setAttribute("contiene-archivo", true);
}

pdfInput.addEventListener("change", event => {
    if (event.target.files.length > 0) {
        archivoAdjuntado(event.target.files[0].name);
    }
});