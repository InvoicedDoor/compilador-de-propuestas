import { handleFileUpload, handleDragOver, handleDragLeave, handleDrop } from "../../pages/project.js";

export const bodyAddCollaboratorsModal = () => {
    const modalBody = document.getElementById("modal-body");
    const sendRequestButton = document.getElementById("send-request-button");

    if (!modalBody)
        return;

    return;

    // modalBody.innerHTML = "";
    // const overlay = document.getElementById("modal-overlay");
    
    // // Cuerpo del modal
    // const inputLabel = document.createElement("label");
    // inputLabel.htmlFor = "mail-input";

    // const mailInput = document.createElement("input");
    // mailInput.type = "text";
    // mailInput.id = "mail-input";
    // mailInput.placeholder = "Ingresa el correo del nuevo colaborador.";

    // const inputGroupContainer = document.createElement("div");
    // inputGroupContainer.className = "input-group";
    // inputGroupContainer.appendChild(inputLabel);
    // inputGroupContainer.appendChild(mailInput);

    // const modalHeader = document.createElement("h3");
    // modalHeader.textContent = "Agregar colaboradores";

    // const addCollaboratorsContainer = document.createElement("div");
    // addCollaboratorsContainer.className = "adjust-complete-width-component";

    // if (!overlay)
    //     return;

    // overlay.style.display = "flex";
    // modalBody.appendChild(addCollaboratorsContainer);
    // sendRequestButton!.textContent = "Agregar colaborador";
}