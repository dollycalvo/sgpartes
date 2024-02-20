const API_ENVIAR_MAIL = window.location.origin + "/enviar_mail";
const formAprobar = document.getElementById("formAprobar");
const hdnIDAprobar = document.getElementById("idPlanillaAprobar");
const botonesVerAprobar = document.querySelectorAll(".btn-success");
const botonesEnviarPorEmail = document.querySelectorAll(".btn-enviar-email");
const dlgEnviandoEmail = document.getElementById("dlgEnviandoEmail");
const dlgResultado = document.getElementById("dlgResultado");

function cerrarModal() {
    dlgResultado.close();
}

for (const boton of botonesVerAprobar) {
    boton.addEventListener("click", e => {
        e.preventDefault();
        hdnIDAprobar.value = boton.id;
        formAprobar.submit();
    });
}

for (const boton of botonesEnviarPorEmail) {
    boton.addEventListener("click", e => {
        e.preventDefault();
        dlgEnviandoEmail.showModal();
        const id_planilla = boton.id;
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
