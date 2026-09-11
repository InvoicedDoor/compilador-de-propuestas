import { UserMemberInterface } from "../../interfaces/userMember.interface.js";
import { modalComponent } from "../modal/modal.js";
import { positionElement } from "./positionElement.js";

export const userMemberRow = (userMember: UserMemberInterface) => {
    const nameParagraph = document.createElement("p");
    nameParagraph.textContent = userMember.name;
    
    const nameColumn = document.createElement("td");
    nameColumn.className = "content-justify";
    nameColumn.appendChild(nameParagraph);
    
    const positionParagraph = document.createElement("p");
    positionParagraph.textContent = userMember.position.position;
    
    const positionColumn = document.createElement("td");
    positionColumn.className = "content-center";
    positionColumn.appendChild(positionParagraph);
    
    const rolParagraph = document.createElement("p");
    rolParagraph.textContent = userMember.rol.rol;
    
    const rolColumn = document.createElement("td");
    rolColumn.className = "content-center";
    rolColumn.appendChild(rolParagraph);
    
    const iconEdit = document.createElement("i");
    iconEdit.className = "action-edit-icon";
    positionElement(iconEdit, modalComponent(), {
        placement: "top"
    })

    const iconCancel = document.createElement("i");
    iconCancel.className = "action-cancel-icon";
    positionElement(iconCancel, modalComponent(), {
        placement: "top"
    })
    
    const iconContainer = document.createElement("div");
    iconContainer.className = "content-image";
    iconContainer.appendChild(iconEdit);
    iconContainer.appendChild(iconCancel);
    
    const imageColumn = document.createElement("td");
    imageColumn.appendChild(iconContainer);

    const newRow = document.createElement("tr");
    newRow.className = "user-info-row";
    newRow.appendChild(nameColumn);
    newRow.appendChild(positionColumn);
    newRow.appendChild(rolColumn);
    newRow.appendChild(imageColumn);
    
    return newRow;
}