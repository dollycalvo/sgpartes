const MSG_EXITO = "exito";
const API_FECHA_LIMITE = window.location.origin + "/fecha_limite";
const API_ESTABLECER_FECHA_LIMITE = window.location.origin + "/establecer_fecha_limite";
const formFechaLimite = document.getElementById("formFechaLimite");
const ddMesLimite = document.getElementById("mesLimite");
const ddAnioLimite = document.getElementById("anioLimite");
const wrapperTxtDiaLimite = document.querySelector(".cargable");
const txtDiaLimite = document.getElementById("txtDiaLimite");
const placeholder = txtDiaLimite.placeholder;
const btnEstablecerFechaLimite = document.getElementById("btnEstablecerFechaLimite");
const csrfToken = document.cookie
                        .split("; ")
                        .find((row) => row.startsWith("csrftoken="))
                        ?.split("=")[1];

// for (const boton of botonesEnviarPorEmail) {
//     boton.addEventListener("click", e => {
//         e.preventDefault();
//         dlgEnviandoEmail.showModal();
//         const id_planilla = boton.id;
//         const csrfToken = document.cookie
//                                 .split("; ")
//                                 .find((row) => row.startsWith("csrftoken="))
//                                 ?.split("=")[1];
//         fetch(API_ENVIAR_MAIL,
//             {
//                 method: "POST",
//                 mode: "cors",
//                 cache: "no-cache",
//                 credentials: "same-origin",
//                 headers: {
//                   "Content-Type": "application/json",
//                   "X-CSRFToken": csrfToken
//                 },
//                 body: JSON.stringify({id_planilla})
//             }
//             )
//             .then(async response => {
//                 if (response.ok === true)
//                     return response.json();
//                 const respuesta = await response.json();
//                 return Promise.reject({"message": `Status Code: ${response.status} (${respuesta.mensaje})`});
//             })
//             .then(data => {
//                 dlgEnviandoEmail.close();
//                 if (data.mensaje == "exito") {
//                     dlgResultado.innerHTML = "El e-mail se ha enviado correctamente.";
//                     dlgResultado.classList.add("modal-exito");
//                 } else {
//                     dlgResultado.innerHTML = data.mensaje;
//                     dlgResultado.classList.add("modal-error");
//                 }
//                 dlgResultado.showModal();
//                 setTimeout(cerrarModal, 3000);
//             })
//             .catch(error => {
//                 dlgEnviandoEmail.close();
//                 dlgResultado.innerHTML = error.message;
//                 dlgResultado.classList.add("modal-error");
//                 dlgResultado.showModal();
//                 setTimeout(cerrarModal, 3000);
//         });
//     });
// }

function mostrarCargando(show) {
    if (show === true) {
        wrapperTxtDiaLimite.setAttribute("cargando", true);
        txtDiaLimite.value = "";
        txtDiaLimite.placeholder = "";
    } else {
        wrapperTxtDiaLimite.removeAttribute("cargando");
        txtDiaLimite.placeholder = placeholder;
    }
}


function recargarFechaLimite() {
    const mes = ddMesLimite.value;
    const anio = ddAnioLimite.value;
    mostrarCargando(true);
    fetch(API_FECHA_LIMITE,
        {
            method: "POST",
            mode: "cors",
            cache: "no-cache",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({mes, anio})
        }
        )
        .then(async response => {
            if (response.ok === true) {
                mostrarCargando(false);
                return response.json();
            }
            const respuesta = await response.json();
            return Promise.reject({"message": `Status Code: ${response.status} (${respuesta.mensaje})`});
        })
        .then(data => {
            if (data.dia) {
                txtDiaLimite.value = data.dia;
            } else {
                txtDiaLimite.value = "";
            }
        })
        .catch(error => {
            mostrarCargando(false);
            console.error(error);
        }
    );
}

ddMesLimite.addEventListener("change", event => {
    recargarFechaLimite();
});

ddAnioLimite.addEventListener("change", event => {
    recargarFechaLimite();
});

function establecerFechaLimite() {
    const diaLimite = txtDiaLimite.value.trim();
    const mes = ddMesLimite.value;
    const anio = ddAnioLimite.value;
    fetch(API_ESTABLECER_FECHA_LIMITE,
        {
            method: "POST",
            mode: "cors",
            cache: "no-cache",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({mes, anio, diaLimite})
        }
        )
        .then(async response => {
            if (response.ok === true)
                return response.json();
            const respuesta = await response.json();
            return Promise.reject({"message": `Status Code: ${response.status} (${respuesta.mensaje})`});
        })
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.error(error);
        }
    );
}

btnEstablecerFechaLimite.addEventListener("click", event => {
    event.preventDefault();
    establecerFechaLimite();
});