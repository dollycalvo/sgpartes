const divNombreUsuario = document.querySelector("#divNombreUsuario");
const btnCerrarSesion = document.querySelector(".btn-cerrar-sesion");
const popupCerrarSesionLarge = document.querySelector("#popup-large");
const popupCerrarSesionSmall = document.querySelector("#popup-small");
const loginIcon = document.querySelector("#infoLogin > div:nth-child(1)");
const loginSection = document.querySelector("#infoLogin");
const logoPersona = document.querySelector(".bi-person-standing");

function changeHands() {
    loginIcon.classList.toggle("bi-person-standing");
    loginIcon.classList.toggle("bi-person-raised-hand");
}

loginSection.addEventListener("mouseover", () => {
    changeHands();
});

loginSection.addEventListener("mouseout", () => {
    changeHands();
});

if (divNombreUsuario) {
    divNombreUsuario.addEventListener("mouseover", () => {
        popupCerrarSesionLarge.classList.add("popup-cerrar-sesion-mostrar-large");
        popupCerrarSesionSmall.classList.add("popup-cerrar-sesion-mostrar-small");
    });
}

if (logoPersona) {
    logoPersona.addEventListener("touchend", () => {
        popupCerrarSesionLarge.classList.add("popup-cerrar-sesion-mostrar-large");
        popupCerrarSesionSmall.classList.add("popup-cerrar-sesion-mostrar-small");
    });
}

if (btnCerrarSesion) {
    btnCerrarSesion.addEventListener("mouseout", () => {
        popupCerrarSesionLarge.classList.remove("popup-cerrar-sesion-mostrar-large");
        popupCerrarSesionSmall.classList.remove("popup-cerrar-sesion-mostrar-small");
    });
}
