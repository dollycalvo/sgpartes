const MSG_EXITO = "exito";
const API_FECHA_LIMITE = window.location.origin + "/fecha_limite";
const API_ESTABLECER_FECHA_LIMITE = window.location.origin + "/establecer_fecha_limite";
const formFechaLimite = document.getElementById("formFechaLimite");
const ddMesLimite = document.getElementById("mesLimite");
const ddAnioLimite = document.getElementById("anioLimite");
const wrapperTxtDiaLimite = document.querySelector(".cargable");
const txtDiaLimite = document.getElementById("txtDiaLimite");
const wrapperInputDiaLimite = document.getElementById("wrapperInputDiaLimite");
const placeholder = txtDiaLimite.placeholder;
const btnEstablecerFechaLimite = document.getElementById("btnEstablecerFechaLimite");
const csrfToken = document.cookie
                        .split("; ")
                        .find((row) => row.startsWith("csrftoken="))
                        ?.split("=")[1];

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

function mostrarSuccess() {
    wrapperInputDiaLimite.setAttribute("success", true);
    setTimeout(() => {
        wrapperInputDiaLimite.removeAttribute("success");
    }, 2000);
}

function mostrarGuardando(mostrar) {
    if (mostrar === false) {
        wrapperInputDiaLimite.removeAttribute("guardando");
    } else {
        wrapperInputDiaLimite.setAttribute("guardando", true);
    }
}

function mostrarError() {
    wrapperInputDiaLimite.setAttribute("error", true);
    setTimeout(() => {
        wrapperInputDiaLimite.removeAttribute("error");
    }, 2000);
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
    mostrarGuardando(true);
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
            mostrarGuardando(false);
            mostrarSuccess();
        })
        .catch(error => {
            console.error(error);
            mostrarGuardando(false);
            mostrarError();
        }
    );
}

btnEstablecerFechaLimite.addEventListener("click", event => {
    event.preventDefault();
    establecerFechaLimite();
});