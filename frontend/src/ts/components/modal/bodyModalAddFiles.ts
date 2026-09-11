import { handleFileUpload, handleDragOver, handleDragLeave, handleDrop } from "../../pages/project.js";

export const bodyAddFilesModal = () => {
    const modalBody= document.getElementById("modal-body");
    const sendRequestButton = document.getElementById("send-request-button");
    
    if (!modalBody)
        return;

    modalBody.innerHTML = "";

    const selectLabel = document.createElement("label");
    selectLabel.className = "select-file-button";
    selectLabel.htmlFor = "images";
    selectLabel.textContent = "Seleccionar archivo";

    const fileInput = document.createElement("input");
    fileInput.className = "files-input";
    fileInput.type = "file";
    fileInput.id = "images";
    fileInput.onchange = (event) => handleFileUpload(event);

    const dropAreaContainer = document.createElement("div");
    dropAreaContainer.className = "drop-area";
    dropAreaContainer.draggable = true;
    dropAreaContainer.ondragover = (event) => handleDragOver(event);
    dropAreaContainer.ondragleave = (event) => handleDragLeave(event);
    dropAreaContainer.ondrop = (event) => handleDrop(event);
    dropAreaContainer.appendChild(selectLabel);
    dropAreaContainer.appendChild(fileInput);

    const uploadImagesDropContainer = document.createElement("div");
    uploadImagesDropContainer.className = "upload-images-drop";
    uploadImagesDropContainer.appendChild(dropAreaContainer);

    const h3Element = document.createElement("h3");
    h3Element.textContent = "Documentos complementarios";

    const inputContainer = document.createElement("div");
    inputContainer.className = "input-container-full-screen";
    inputContainer.appendChild(h3Element);
    inputContainer.appendChild(uploadImagesDropContainer);

    const filesContainerFullScreen = document.createElement("div");
    filesContainerFullScreen.className = "files-container-full-screen no-show-files";
    filesContainerFullScreen.id = "show_files_container";

    const uploadFilesContainer = document.createElement("div");
    uploadFilesContainer.className = "upload-files-container";
    uploadFilesContainer.appendChild(filesContainerFullScreen);
    uploadFilesContainer.appendChild(inputContainer);

    const overlay = document.getElementById("modal-overlay");
    
    if (!overlay)
        return;

    overlay.style.display = "flex";
    modalBody.appendChild(uploadFilesContainer);
    sendRequestButton!.textContent = "Agregar archivos";
}