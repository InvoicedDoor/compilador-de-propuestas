import projectInfoStore from "../../storages/projectInfoStorage.js";
import { modalComponent } from "../modal/modal.js";

export const leftBarComponent = () => {
    try
    {
        const projectEvents = projectInfoStore.store.project_events;

        console.log(projectEvents)

        // Obtener la sección de la barra lateral izquierda.
        const leftBarContainer = document.getElementById("left-bar");
        
        // Retornar si la sección no existe.
        if (!leftBarContainer)
            return;
        
        // Retornar si ya tiene contenido.
        if (leftBarContainer.hasChildNodes())
            return;
        
        /* ============== Header ============== */
        const leftBarTitle = document.createElement("h3");
        leftBarTitle.textContent = "Acciones";
        
        const leftBarHeader = document.createElement("div");
        leftBarHeader.className = "actions-header"
        leftBarHeader.appendChild(leftBarTitle);
        
        /* ============== Body ============== */
        const container = document.createElement("div");
        container.className = "left-bar-body";
        if (projectEvents.length === 0)
        {
            const emptyBody = document.createElement("span");
            emptyBody.textContent = "No hay eventos recientes.";
            container.appendChild(emptyBody);
        } else
        {
            const bodyLeftBar = document.createElement("div");
            bodyLeftBar.className = "event-container user-wrapper";
            for (let event = 0; event < projectEvents.length; event++) {
                /* ==================== Event row container ==================== */
                const eventRow = document.createElement("div");
                eventRow.className = "event-row";
                
                /* ===================== Username field ===================== */
                const usernameEventParagraph = document.createElement("p");
                usernameEventParagraph.className = "event-field";
                usernameEventParagraph.textContent = `${projectEvents[event].name} ${projectEvents[event].first_lastname} ${projectEvents[event].second_lastname ?? ""}`;
                
                /* ===================== User action field ===================== */
                const userSelectionParagraph = document.createElement("p");
                userSelectionParagraph.className = "event-field";
                userSelectionParagraph.textContent = projectEvents[event].approved ? "Aprobado" : "Denegado";
                
                /* ===================== User role field ===================== */
                const userRoleParagraph = document.createElement("p");
                userRoleParagraph.className = "event-field";
                userRoleParagraph.textContent = projectEvents[event].role.role;

                /* =================== Append child elements =================== */
                eventRow.appendChild(usernameEventParagraph);
                eventRow.appendChild(userRoleParagraph);
                eventRow.appendChild(userSelectionParagraph);
                
                // /* ===================== Modal wrapper ===================== */
                // const modalWrapper = document.createElement("div");
                // modalWrapper.className = "user-wrapper";
                // modalWrapper.onmouseenter = (event: MouseEvent) => hoverUserInformation(event);
                // modalWrapper.onmouseleave = (event: MouseEvent) => leaveHoverUserInformation(event);
                
                /* ===================== Modal space ===================== */
                const modalInfoSection = document.createElement("div");
                modalInfoSection.className = "modal-space";
                modalInfoSection.id = "modal-event-info";
                modalInfoSection.onmouseenter = (event: MouseEvent) => hoverUserInformation(event);
                modalInfoSection.onmouseleave = (event: MouseEvent) => leaveHoverUserInformation(event);
                bodyLeftBar.appendChild(eventRow);
                bodyLeftBar.appendChild(modalInfoSection);
            }
            container.appendChild(bodyLeftBar);
        }

        // Acoplar los elementos en el orden correcto
        leftBarContainer.appendChild(leftBarHeader); // Header
        leftBarContainer.appendChild(container); // Body

    } catch (e)
    {
        console.error(e);
    }
}

declare global {
    interface Window {
        leftBarComponent: () => void;
    }
}

window.leftBarComponent = leftBarComponent;

/* ===================== EVENTS ===================== */
const hoverUserInformation = (event: MouseEvent): void => {
    console.log("Evento realizado.")
    console.log(event)

    return

    // const container = document.getElementById(`modal-event-info-${event.target.id}`);

    // if (!container) return;

    // if (container.querySelector(".modal-card")) return;

    // const modal = modalComponent();
    // container.appendChild(modal);
};

const leaveHoverUserInformation = (event: MouseEvent): void => {
    const wrapper = event.currentTarget as HTMLElement;
    const modal = wrapper.querySelector(".modal-card");

    if (modal) {
        modal.remove();
    }
};