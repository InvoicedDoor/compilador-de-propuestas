/*<div class="app-main-image-container">
    <img class="app-main-logo" src="/icons/proposal-manager.png" alt="" onclick="window.location.href='/'">
</div>
<div class="navbar-options">
    <img class="icon-option" src="/icons/table-solid.svg" alt="Redirección a la tabla de propuestas">
    <img class="icon-option" src="/icons/table-solid.svg" alt="Redirección a agregar propuesta">
</div>
<div class="user-wrapper"
onmouseenter="hoverUserInformation(event)"
onmouseleave="leaveHoverUserInformation(event)">
    <div class="user-identification">
        <div class="user-image">
            <img src="/icons/user-solid.svg" alt="">
        </div>
        <div class="user-name">
            <h4>Bienvenido: <p>Dónovan Hernández</p>
            </h4>
        </div>
    </div>
    <div id="modal-space" class="modal-space"></div>
</div>*/
import { modalComponent } from "./modal.js";
export const navBarComponent = (userName) => {
    const navbarContainer = document.getElementById("navbar");
    if (!navbarContainer) {
        throw new Error("Navbar container no existe");
    }
    if (navbarContainer.hasChildNodes())
        return;
    /* ===================== LOGO ===================== */
    const mainLogo = document.createElement("div");
    mainLogo.className = "app-main-image-container";
    const imageLogo = document.createElement("img");
    imageLogo.className = "app-main-logo";
    imageLogo.src = "/icons/proposal-manager.png";
    imageLogo.alt = "Application Logo";
    imageLogo.onclick = () => window.location.href = '/';
    mainLogo.appendChild(imageLogo);
    /* ===================== OPTIONS ===================== */
    const navbarOptions = document.createElement("div");
    navbarOptions.className = "navbar-options";
    const proposalTableOption = document.createElement("img");
    proposalTableOption.className = "icon-option";
    proposalTableOption.src = "/icons/table.svg";
    proposalTableOption.alt = "Tabla de propuestas";
    proposalTableOption.onclick = () => window.location.href = '/';
    const addProposalOption = document.createElement("img");
    addProposalOption.className = "icon-option";
    addProposalOption.src = "/icons/plus.svg";
    addProposalOption.alt = "Agregar propuesta";
    addProposalOption.onclick = () => window.location.href = '/html/add-proposal.html';
    navbarOptions.appendChild(proposalTableOption);
    navbarOptions.appendChild(addProposalOption);
    /* ===================== USER ===================== */
    const userInformation = document.createElement("div");
    userInformation.className = "user-wrapper";
    userInformation.onmouseenter = (event) => hoverUserInformation(event);
    userInformation.onmouseleave = (event) => leaveHoverUserInformation(event);
    const userIdentificationContainer = document.createElement("div");
    userIdentificationContainer.className = "user-identification";
    const userImageContainer = document.createElement("div");
    userImageContainer.className = "user-image";
    const userImage = document.createElement("img");
    userImage.src = "/icons/user-solid.svg";
    userImage.alt = "Imagen de usuario";
    const userNameContainer = document.createElement("div");
    userNameContainer.className = "user-name";
    const h4 = document.createElement("h4");
    const p = document.createElement("p");
    h4.textContent = "Bienvenido: ";
    p.textContent = userName;
    h4.appendChild(p);
    userNameContainer.appendChild(h4);
    userImageContainer.appendChild(userImage);
    userIdentificationContainer.appendChild(userImageContainer);
    userIdentificationContainer.appendChild(userNameContainer);
    const modalSpace = document.createElement("div");
    modalSpace.className = "modal-space";
    userInformation.appendChild(userIdentificationContainer);
    userInformation.appendChild(modalSpace);
    /* ===================== APPEND ===================== */
    navbarContainer.appendChild(mainLogo);
    navbarContainer.appendChild(navbarOptions);
    navbarContainer.appendChild(userInformation);
};
/* ===================== EVENTS ===================== */
const hoverUserInformation = (event) => {
    const wrapper = event.currentTarget;
    const container = wrapper.querySelector(".modal-space");
    if (!container)
        return;
    if (container.querySelector(".modal-card"))
        return;
    const modal = modalComponent();
    container.appendChild(modal);
};
const leaveHoverUserInformation = (event) => {
    const wrapper = event.currentTarget;
    const modal = wrapper.querySelector(".modal-card");
    if (modal) {
        modal.remove();
    }
};
