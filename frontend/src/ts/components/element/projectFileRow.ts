import { deleteInfo } from "../../functions/apiConnection.js";
import { FileInterface } from "../../interfaces/file.interface.js";
import { modalComponent } from "../modal/modal.js";
import { showToast } from "../modal/notifications.js";
import { positionElement } from "./positionElement.js";

export const projectFileRow = (projectId: number, projectFile: FileInterface, handleClickFunction: (projectId: number, fileId: number) => Promise<void>) => {
    const infoContainer = document.createElement("div");
    infoContainer.className = "info-container";

    const filenameContainer = document.createElement("div");
    filenameContainer.className = "filename-container";

    const pFilenameElement = document.createElement("div");
    pFilenameElement.textContent = projectFile.filename;

    const actionContent = document.createElement("div");
    actionContent.className = "action-content";
    
    const actionDownloadIcon = document.createElement("i");
    actionDownloadIcon.className = "action-download-icon";
    positionElement(actionDownloadIcon, modalComponent(), {
        placement: "top"
    })

    const actionDeleteIcon = document.createElement("i");
    actionDeleteIcon.className = "action-delete-icon";
    actionDeleteIcon.onclick = async () => await handleClickFunction(projectId, projectFile.id)

    positionElement(actionDeleteIcon, modalComponent(), {
        placement: "top"
    })

    const listElement = document.createElement("li");
    listElement.className = "file-element-list";

    filenameContainer.appendChild(pFilenameElement);

    actionContent.appendChild(actionDownloadIcon);
    actionContent.appendChild(actionDeleteIcon);
    
    infoContainer.appendChild(filenameContainer);
    infoContainer.appendChild(actionContent);

    listElement.appendChild(infoContainer);

    return listElement;
}