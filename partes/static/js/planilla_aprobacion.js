const API_ENVIAR_MAIL = window.location.origin + "/enviar_mail";
const id_planilla = document.getElementById("hdnIdPlanilla").value;
const formAprobar = document.querySelector("#formAprobar");
const btnAprobar = document.getElementById("btnAprobar");
const btnRevisar = document.getElementById("btnRevisar");
const hdnAprobar = document.getElementById("hdnAprobar");
const txtObservaciones = document.getElementById("txtObservaciones");
const btnEnviar = document.getElementById("btnEnviar");
const dlgEnviandoEmail = document.getElementById("dlgEnviandoEmail");
const dlgResultado = document.getElementById("dlgResultado");

function cerrarModal() {
    dlgResultado.close();
}

if (btnAprobar) {
    btnAprobar.addEventListener("click", event => {
        event.preventDefault();
        if (confirm("¿Confirma que desea aprobar la presente planilla?")) {
            hdnAprobar.value = 1;
            formAprobar.submit();
        }
    });
}

if (btnRevisar) {
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
}

if (btnEnviar) {
    btnEnviar.addEventListener("click", e => {
        e.preventDefault();
        dlgEnviandoEmail.showModal();
        const csrfToken = document.cookie
                                .split("; ")
                                .find((row) => row.startsWith("csrftoken="))
                                ?.split("=")[1];
        fetch(API_ENVIAR_MAIL,
            {
                method: "POST",
                mode: "cors",
                cache: "no-cache",
                credentials: "same-origin",
                headers: {
                  "Content-Type": "application/json",
                  "X-CSRFToken": csrfToken
                },
                body: JSON.stringify({id_planilla})
            }
            )
            .then(async response => {
                if (response.ok === true)
                    return response.json();
                const respuesta = await response.json();
                return Promise.reject({"message": `Status Code: ${response.status} (${respuesta.mensaje})`});
            })
            .then(data => {
                dlgEnviandoEmail.close();
                if (data.mensaje == "exito") {
                    dlgResultado.innerHTML = "El e-mail se ha enviado correctamente.";
                    dlgResultado.classList.add("modal-exito");
                } else {
                    dlgResultado.innerHTML = data.mensaje;
                    dlgResultado.classList.add("modal-error");
                }
                dlgResultado.showModal();
                setTimeout(cerrarModal, 3000);
            })
            .catch(error => {
                dlgEnviandoEmail.close();
                dlgResultado.innerHTML = error.message;
                dlgResultado.classList.add("modal-error");
                dlgResultado.showModal();
                setTimeout(cerrarModal, 3000);
        });
    });
}
