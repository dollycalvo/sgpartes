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
const STATUS_PLANILLA = {borrador: "Borrador", presentado: "Presentado", aprobado: "Aprobado"};
const statusPlanilla = document.getElementById("hdnStatusPlanilla").value;
let indiceArchivo = 0;
// Este array tendrá los índices de los archivos que se vayan eliminando, y previo a submit se eliminarán
const archivosEliminados = []; 

btnLimpiarForm.addEventListener("click", () => {
    if (confirm("¿Confirma que desea limpiar el formulario? Se eliminarán todos los comentarios y el archivo adjunto.")) {
        const inputs = document.querySelectorAll("input.input-registro-diario");
        inputs.forEach(input => input.value = "");
        const selects = document.querySelectorAll("select.input-registro-diario");
        selects.forEach(sel => sel.value = S_N);
        todosArchivosEliminados();
    }
});

btnGuardarCambios.addEventListener("click", event => {
    event.preventDefault();
    hdnAccionSubmit.value = opcionesAccionesSubmit[0];
    procesarArchivosAdjuntos();
    formPlanilla.submit();
});

btnPresentarPlanilla.addEventListener("click", () => {
    if (confirm("¿Confirma que desea presentar la planilla?\nUna vez presentada, los datos se enviarán a su supervisor y no podrá ser modificada.")) {
        hdnAccionSubmit.value = opcionesAccionesSubmit[1];
        procesarArchivosAdjuntos();
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
        areaAdjunto.insertBefore(componenteArchivoAdjunto(archivo.name), dummyAdjuntarArchivo);
    }
    pdfInput.files = archivos;
    if (statusPlanilla == STATUS_PLANILLA.borrador) {
        btnPresentarPlanilla.removeAttribute("disabled");
    }
}

function componenteArchivoAdjunto(nombre) {
    // Div wrapper
    const div = document.createElement("div");
    div.className = "wrapperNombreArchivo";
    div.id = "new_" + indiceArchivo++;
    // Icono PDF
    const i = document.createElement("i");
    i.className = "bi bi-file-earmark-pdf";
    div.appendChild(i);
    // Nombre del archivo, no es anchor porque no necesito descargarlo
    const innerDiv = document.createElement("div");
    innerDiv.textContent = nombre;
    div.appendChild(innerDiv);
    // Botón eliminar
    const btnCerrar = document.createElement("div");
    btnCerrar.addEventListener("click", event => {
        if (confirm(`¿Confirmás que deseás eliminar el archivo "${nombre}"?`)) {
            document.getElementById(event.target.parentNode.id).remove();
            // Lo quitamos del input
            for (let i = 0; i < pdfInput.files.length; i++) {
                if (pdfInput.files[i].name === nombre) {
                    archivosEliminados.push(i);
                }
            }
        }
    });
    btnCerrar.innerHTML = "&times;";
    btnCerrar.className = "wrapperArchivoCerrar";
    div.appendChild(btnCerrar);
    return div;
}

function todosArchivosEliminados() {
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

function eliminarArchivo(event) {
    event.stopPropagation();
    alert("click");
}

function procesarArchivosAdjuntos() {
    const dt = new DataTransfer();
    const { files } = pdfInput;
    for (let i = 0; i < files.length; i++) {
        if (! archivosEliminados.includes(i)) {
            dt.items.add(files[i]);
        }
    }
    pdfInput.files = dt.files;
}