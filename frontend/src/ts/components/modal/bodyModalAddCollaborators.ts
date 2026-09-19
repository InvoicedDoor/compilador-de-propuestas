import invitationStore, { InvitationInterface } from "../../storages/invitationsStorage.js";
import projectRolesStore from "../../storages/projectRolesStorage.js";
import { showToast } from "./notifications.js";

(async () => {
    await projectRolesStore.projectRolesActions.loadInfo();
})();

const modelBase: InvitationInterface = {
    mail: "",
    project_role: ""
}

let invitation = modelBase;

const handleInputMail = (event: InputEvent) => {
    const target = event.target as HTMLInputElement
    invitation.mail = target.value;
}

const handleInputRole = (event: Event) => {
    const target = event.target as HTMLInputElement
    invitation.project_role = target.value;
}

const handleAppendinvitation = () => {
    if (invitation.mail === "" || invitation.project_role === "")
    {
        showToast("Debes ingresar un correo y su rol en el proyecto.", "info")
        return;
    }

    if (invitationStore.store.users.find(user => user.mail === invitation.mail))
    {
        showToast("El usuario ya tiene una invitación cargada.", "warning")
        return;
    }

    invitationStore.invitationActions.addUser({...invitation});
    
    const mailInput = document.getElementById("mail-input") as HTMLInputElement;
    mailInput!.value = "";
    
    const roleInput = document.getElementById("role-input") as HTMLSelectElement;
    roleInput!.value = "";

    invitation.mail = "";
    invitation.project_role = "";
}

const handleSendinvitations = () => {
    console.log(invitationStore.store.users)
}

export const bodyAddCollaboratorsModal = () => {
    const modalBody = document.getElementById("modal-body");
    
    if (!modalBody)
        return;
        
    modalBody.innerHTML = "";
    const overlay = document.getElementById("modal-overlay");
    if (!overlay)
        return;
    
    // Cuerpo del modal
    /* Input email */
    const inputLabel = document.createElement("label");
    inputLabel.htmlFor = "mail-input";
    
    const mailInput = document.createElement("input");
    mailInput.type = "email";
    mailInput.className = "mail-input";
    mailInput.id = "mail-input";
    mailInput.placeholder = "Ingresa el correo del nuevo colaborador.";
    mailInput.oninput = handleInputMail;

    const inputGroupContainer = document.createElement("div");
    inputGroupContainer.className = "input-group";
    inputGroupContainer.appendChild(inputLabel);
    inputGroupContainer.appendChild(mailInput);
    
    /* Input role */
    const selectRoleLabel = document.createElement("label");
    selectRoleLabel.htmlFor = "role-input";
    selectRoleLabel.textContent = "Role";

    const selectRole = document.createElement("select");
    selectRole.name = "role-input";
    selectRole.id = "role-input";
    selectRole.className = "select-user-role adjust-complete-width-component";
    selectRole.onchange = handleInputRole;
    
    const defaultOption = document.createElement("option");
    defaultOption.textContent = "Selecciona un rol";
    defaultOption.value = "";
    defaultOption.selected = true;
    defaultOption.disabled = true;
    selectRole.appendChild(defaultOption);
    
    projectRolesStore.store.roles.map(role => {
        const option = document.createElement("option");
        option.value = role.code;
        option.textContent = role.description;
        selectRole.appendChild(option);
    })

    const selectRoleContainer = document.createElement("div");
    selectRoleContainer.className = "input-add-invitation adjust-complete-width-component";
    selectRoleContainer.appendChild(selectRole);
    
    const inputGroupSelectContainer = document.createElement("div");
    inputGroupSelectContainer.className = "input-group";
    inputGroupSelectContainer.appendChild(selectRoleContainer);
    
    /* Button add */
    const buttonAddImage = document.createElement("i");
    buttonAddImage.className = "icon-style plus-icon size-height-30";

    const buttonAdd = document.createElement("button");
    buttonAdd.className = "add-invitation-button adjust-complete-width-component";
    buttonAdd.onclick = handleAppendinvitation;
    buttonAdd.appendChild(buttonAddImage);
    
    const buttonAddContainer = document.createElement("div");
    buttonAddContainer.className = "input-group display-flex justify-content-center align-items-center";
    buttonAddContainer.appendChild(buttonAdd);

    /* Modal header */
    const modalHeader = document.createElement("h3");
    modalHeader.textContent = "Agregar colaboradores";

    /* Colaborators container */
    const showAddCollaboratorsContainer = document.createElement("div");
    showAddCollaboratorsContainer.className = "show-new-collaborators-mail";
    showAddCollaboratorsContainer.textContent = "No hay colaboradores";
    
    /* Integrar los elementos al contenedor principal */
    const addCollaboratorsContainer = document.createElement("div");
    addCollaboratorsContainer.className = "adjust-complete-width-component";
    addCollaboratorsContainer.appendChild(modalHeader);
    addCollaboratorsContainer.appendChild(inputGroupContainer);
    addCollaboratorsContainer.appendChild(inputGroupSelectContainer);
    addCollaboratorsContainer.appendChild(buttonAddContainer);
    addCollaboratorsContainer.appendChild(showAddCollaboratorsContainer);
    
    overlay.style.display = "flex";
    modalBody.appendChild(addCollaboratorsContainer);
    
    const sendRequestButton = document.getElementById("send-request-button");
    sendRequestButton!.textContent = "Agregar colaborador";
}