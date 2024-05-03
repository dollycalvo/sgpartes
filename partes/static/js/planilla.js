const formPlanilla = document.querySelector("#formPlanilla");
const btnLimpiarForm = document.querySelector("#btnLimpiarForm");
const btnGuardarCambios = document.querySelector("#btnGuardarCambios");
const btnPresentarPlanilla = document.querySelector("#btnPresentarPlanilla");
const hdnAccionSubmit = document.querySelector("#hdnAccionSubmit");
const opcionesAccionesSubmit = hdnAccionSubmit.getAttribute("opciones").split("#");
const dummyAdjuntarArchivo = document.getElementById("dummyAdjuntarArchivo");
const areaAdjunto = document.getElementById("area-adjunto");
const pdfInput = document.getElementById("pdf");
const spansFachadaSelects = document.querySelectorAll(".spanFachadaSelect");
const selectsCodigos = document.getElementsByName("codigos");
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

dummyAdjuntarArchivo.addEventListener("dragover", event => {
    event.preventDefault();
    dummyAdjuntarArchivo.classList.add("file-drag-over");
    dummyAdjuntarArchivo.classList.remove("filter-full-grayscale", "opacity05");
});

dummyAdjuntarArchivo.addEventListener("dragleave", event => {
    event.preventDefault();
    dummyAdjuntarArchivo.classList.remove("file-drag-over");
    dummyAdjuntarArchivo.classList.add("filter-full-grayscale", "opacity05");
});

dummyAdjuntarArchivo.addEventListener("drop", event => {
    event.preventDefault();
    dummyAdjuntarArchivo.classList.remove("file-drag-over");
    dummyAdjuntarArchivo.classList.add("filter-full-grayscale", "opacity05");
    archivosAdjuntado(event.dataTransfer.files);
});

dummyAdjuntarArchivo.addEventListener("click", () => {
    fileInputOpen();
});

function fileInputOpen() {
    pdfInput.click();
}

function archivosAdjuntado(archivos) {
    for (let archivo of archivos) {
        areaAdjunto.innerHTML = componenteArchivoAdjunto(archivo.name) + areaAdjunto.innerHTML;
    }
    pdfInput.files = archivos;
    btnPresentarPlanilla.removeAttribute("disabled");
}

function componenteArchivoAdjunto(nombre) {
    return `
        <div id="wrapperNombreArchivo">
            <i class='bi bi-file-earmark-pdf'></i>
            <div id="nombreArchivo">${nombre}</div>
        </div>
    `;
}

function archivoEliminado() {
    const wrapperNombreArchivo = document.getElementById("wrapperNombreArchivo");
    wrapperNombreArchivo.classList.add("d-none");
    dummyAdjuntarArchivo.classList.remove("d-none");
    areaAdjunto.setAttribute("contiene-archivo", false);
    pdfInput.value = null;
    btnPresentarPlanilla.setAttribute("disabled", true);
}

pdfInput.addEventListener("change", event => {
    if (event.target.files.length > 0) {
        archivosAdjuntado(event.target.files);
    }
});

selectsCodigos.forEach((select, index) => {    
    select.addEventListener("change", event => {
        spansFachadaSelects[index].textContent = event.target[event.target.selectedIndex].getAttribute("data-codigo");
    });
});