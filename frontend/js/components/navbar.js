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

import { modalComponent } from "../components/modal.js";

export const navBarComponent = (userName) => {

    const navbarContainer = document.getElementById("navbar");

    if (navbarContainer.hasChildNodes())
        return;

    // Agregar logo de la aplicación
    const mainLogo = document.createElement("div");
    mainLogo.className = "app-main-image-container";

    const imageLogo = document.createElement("img");
    imageLogo.className = "app-main-logo";
    imageLogo.src = "/icons/proposal-manager.png";
    imageLogo.alt = "Application Logo";
    imageLogo.onclick = () => window.location.href = '/';

    const navbarOptions = document.createElement("div");
    navbarOptions.className = "navbar-options"

    const proposalTableOption = document.createElement("img");
    proposalTableOption.className = "icon-option";
    proposalTableOption.src = "/icons/table-solid.svg";
    proposalTableOption.alt = "Redirección a la tabla de propuestas";
    proposalTableOption.onclick = () => window.location.href = '/';
    
    const addProposalOption = document.createElement("img");
    addProposalOption.className = "icon-option";
    addProposalOption.src = "/icons/plus.svg";
    addProposalOption.alt = "Redirección a agregar propuesta";
    addProposalOption.onclick = () => window.location.href = '/html/add-proposal.html';

    const userInformation = document.createElement("div");
    userInformation.className = "user-wrapper";
    userInformation.onmouseenter =(event) => hoverUserInformation(event);
    userInformation.onmouseleave = (event) => leaveHoverUserInformation(event);

    const userIdentificationContainer = document.createElement("div");
    userIdentificationContainer.className = "user-identification";
    const userIdentificationImageContainer = document.createElement("div");
    userIdentificationImageContainer.className = "user-image";
    const userIdentificationImage = document.createElement("img");
    userIdentificationImage.src = "/icons/user-solid.svg";
    userIdentificationImage.alt = "Imagen de usaurio.";
    const userIdentificationNameContainer = document.createElement("div");
    userIdentificationNameContainer.className = "user-name";
    const h4Element = document.createElement("h4");
    const pElement = document.createElement("p");
    pElement.textContent = userName;
    h4Element.textContent = "Bienvenido: ";

    const modalSpace = document.createElement("div");
    modalSpace.className = "modal-space";
    modalSpace.id = "modal-space";

    userIdentificationImageContainer.appendChild(userIdentificationImage);

    h4Element.appendChild(pElement);
    userIdentificationNameContainer.appendChild(h4Element);

    userIdentificationContainer.appendChild(userIdentificationImageContainer);
    userIdentificationContainer.appendChild(userIdentificationNameContainer);
    userInformation.appendChild(userIdentificationContainer);
    userInformation.appendChild(modalSpace);

    mainLogo.appendChild(imageLogo);

    navbarOptions.appendChild(proposalTableOption);
    navbarOptions.appendChild(addProposalOption);

    navbarContainer.appendChild(mainLogo);
    navbarContainer.appendChild(navbarOptions);
    navbarContainer.appendChild(userInformation);
}

const hoverUserInformation = (event) => {
    const wrapper = event.currentTarget;
    const container = wrapper.querySelector(".modal-space");

    if (container.querySelector(".modal-card")) return;

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

