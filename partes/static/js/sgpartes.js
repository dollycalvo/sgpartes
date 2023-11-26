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