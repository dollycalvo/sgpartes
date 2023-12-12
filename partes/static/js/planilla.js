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
    if (confirm("¿Confirma que desea limpiar el formulario? Se eliminarán todos los comentarios y el archivo adjunto.")) {
        const inputs = document.querySelectorAll("input.input-registro-diario");
        inputs.forEach(input => input.value = "");
        const selects = document.querySelectorAll("select.input-registro-diario");
        selects.forEach(sel => sel.value = S_N);
        archivoEliminado();
    }
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
    event.preventDefault();
    noFilesSelectedText.classList.remove("file-drag-over");
    if (event.dataTransfer.files.length != 1) {
        return alert("Sólo un archivo puede ser adjuntado. Por favor intente nuevamente.");
    }
    archivoAdjuntado(event.dataTransfer.files);
});

function fileInputOpen() {
    pdfInput.click();
}

function archivoAdjuntado(archivos) {
    const wrapperNombreArchivo = document.getElementById("wrapperNombreArchivo");
    const nombreArchivo = document.getElementById("nombreArchivo");
    nombreArchivo.innerHTML = archivos[0].name;
    wrapperNombreArchivo.classList.remove("d-none");
    noFilesSelectedText.classList.add("d-none");
    areaAdjunto.setAttribute("contiene-archivo", true);
    pdfInput.files = archivos;
    btnPresentarPlanilla.removeAttribute("disabled");
}

function archivoEliminado() {
    const wrapperNombreArchivo = document.getElementById("wrapperNombreArchivo");
    wrapperNombreArchivo.classList.add("d-none");
    noFilesSelectedText.classList.remove("d-none");
    areaAdjunto.setAttribute("contiene-archivo", false);
    pdfInput.value = null;
    btnPresentarPlanilla.setAttribute("disabled", true);
}

pdfInput.addEventListener("change", event => {
    if (event.target.files.length > 0) {
        archivoAdjuntado(event.target.files);
    }
});