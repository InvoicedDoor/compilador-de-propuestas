import { modalComponent } from "../modal/modal.js";

export const navBarComponent = (userName: string): void => {

    const navbarContainer = document.getElementById("navbar");

    if (!navbarContainer) {
        throw new Error("Navbar container no existe");
    }

    if (navbarContainer.hasChildNodes()) return;

    /* ===================== LOGO ===================== */

    const mainLogo = document.createElement("div");
    mainLogo.className = "app-main-image-container";

    const imageLogo = document.createElement("img");
    imageLogo.className = "app-main-logo";
    imageLogo.src = "/icons/project-manager.png";
    imageLogo.alt = "Application Logo";
    imageLogo.onclick = () => window.location.href = '/';
    mainLogo.appendChild(imageLogo);

    /* ===================== OPTIONS ===================== */

    const navbarOptions = document.createElement("div");
    navbarOptions.className = "navbar-options";

    const projectTableOption = document.createElement("img");
    projectTableOption.className = "icon-option";
    projectTableOption.src = "/icons/table.svg";
    projectTableOption.alt = "Tabla de propuestas";
    projectTableOption.onclick = () => window.location.href = '/';

    const addProjectOption = document.createElement("img");
    addProjectOption.className = "icon-option";
    addProjectOption.src = "/icons/plus.svg";
    addProjectOption.alt = "Agregar propuesta";
    addProjectOption.onclick = () => window.location.href = '/html/add-project.html';

    navbarOptions.appendChild(projectTableOption);
    navbarOptions.appendChild(addProjectOption);

    /* ===================== USER ===================== */

    const userInformation = document.createElement("div");
    userInformation.className = "user-wrapper";

    userInformation.onmouseenter = (event: MouseEvent) => hoverUserInformation(event);
    userInformation.onmouseleave = (event: MouseEvent) => leaveHoverUserInformation(event);

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

    navbarOptions.appendChild(userInformation);

    /* ===================== APPEND ===================== */

    navbarContainer.appendChild(mainLogo);
    navbarContainer.appendChild(navbarOptions);
};

/* ===================== EVENTS ===================== */

const hoverUserInformation = (event: MouseEvent): void => {
    const wrapper = event.currentTarget as HTMLElement;
    const container = wrapper.querySelector(".modal-space");

    if (!container) return;

    if (container.querySelector(".modal-card")) return;

    const modal = modalComponent();
    container.appendChild(modal);
};

const leaveHoverUserInformation = (event: MouseEvent): void => {
    const wrapper = event.currentTarget as HTMLElement;
    const modal = wrapper.querySelector(".modal-card");

    if (modal) {
        modal.remove();
    }
};