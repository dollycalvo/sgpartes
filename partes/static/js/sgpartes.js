const divNombreUsuario = document.querySelector("#divNombreUsuario");
const popupCerrarSesion = document.querySelector(".popup-cerrar-sesion");
const loginIcon = document.querySelector("#infoLogin > div:nth-child(1)");
const loginSection = document.querySelector("#infoLogin");

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
        popupCerrarSesion.classList.add("popup-cerrar-sesion-mostrar");
    });
}

if (popupCerrarSesion) {
    popupCerrarSesion.addEventListener("mouseout", () => {
        popupCerrarSesion.classList.remove("popup-cerrar-sesion-mostrar");
    });
}
