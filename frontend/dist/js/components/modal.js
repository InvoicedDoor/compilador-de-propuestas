export const modalComponent = () => {
    const container = document.createElement("div");
    container.className = "modal-card";
    container.innerHTML =
        `<ul class="options-list">
            <li>Perfil</li>
            <li>Configuración</li>
            <li id="close-session">Cerrar sesión</li>
        </ul>`;
    const closeSessionButton = container.querySelector("#close-session");
    if (closeSessionButton) {
        closeSessionButton.addEventListener("click", closeSession);
    }
    return container;
};
const closeSession = () => {
    localStorage.clear();
    window.location.href = "/html/login.html";
};
