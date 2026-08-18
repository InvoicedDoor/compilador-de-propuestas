
import { proposalFileRow } from "../components/element/proposalFileRow.js";
import { userMemberRow } from "../components/element/userMemberRow.js";
import { getInfo, uploadInfo } from "../functions/apiConnection.js";
import { verifyAuth } from "../functions/verifyAuth.js";
import { createFileOption } from "../components/element/fileTypeButton.js";
import { FileInterface, Metadata, Preview } from "../interfaces/file.interface.js";
import { UserMemberInterface } from "../interfaces/userMember.interface.js";
import FileTypeModel from "../models/fileType.model.js";
import { showToast } from "../components/modal/notifications.js";
import { pageIndexList } from "../components/element/page-index-list.js";

/* ===================== AUTH ===================== */

const token: string = localStorage.getItem("token") ?? "";

if (!token) {
    window.location.href = "/html/login.html";
}

verifyAuth(token);

/* ===================== STATE ===================== */
let fileTypes: FileTypeModel[] = [];

const params = new URLSearchParams(window.location.search);
const projectId: number = Number(params.get("id")) || 0;
let proposalInfo: any = null;
let membersInfo: any = [];
let filesInfo: Array<FileInterface> = [];
const proposalTitleElement = document.getElementById("project-title");
const proposalDescriptionElement = document.getElementById("project-description");
const proposalFiles = document.getElementById("file-list-element");

const selectedFiles: File[] = [];
const metadatos: Metadata[] = [];
const previewUrls: Preview[] = [];


const imagesContainer = document.getElementById("show_files_container") as HTMLElement;
let proposalTitle: string = "";
let proposalDescription: string = "";
let temporalId: number = 1;
let filePage = 1;
let totalPages = 1;

/* ===================== RENDER ===================== */
const processFiles = (files: FileList): void => {

    for (let i = 0; i < files.length; i++) {
        let isAllowed = false
        const file = files[i];

        const exists = selectedFiles.find(f =>
            f.name === file.name &&
            f.size === file.size &&
            f.lastModified === file.lastModified
        );

        if (exists) {
            alert("Archivo ya existente.");
            continue;
        }

        fileTypes.map(type => {
            if (file.name.includes(type.mime.extension) && !isAllowed) {
                selectedFiles.push(file);

                previewUrls.push({
                    id: temporalId,
                    url: URL.createObjectURL(file),
                });

                metadatos.push({
                    id: temporalId,
                    type: file.type,
                    name: file.name
                });

                temporalId++;
                isAllowed = true;
            }

        });

        if (!isAllowed)
            alert(`El archivo ${file.name} no está permitido.`);

        isAllowed = false;
    }

    loadFilesOnContainer();

    imagesContainer.classList.replace("no-show-files", "show-files");
};

const chargeFileList = (startCount: number, endCount: number) => {
    for (let pageCount = startCount; pageCount < endCount; pageCount++)
    {
        if (pageCount > endCount || pageCount >= filesInfo.length)
        {
            return;
        }

        let rowFile = proposalFileRow(filesInfo[pageCount]);

        proposalFiles?.appendChild(rowFile);
    }
}

const loadFilesOnContainer = (): void => {
    imagesContainer.innerHTML = "";

    for (let count = 0; count < previewUrls.length; count++) {
        const container = document.createElement("div");
        container.className = "file-item";

        const typeFileSelect = document.createElement("select");
        typeFileSelect.className = "type-file-select";
        typeFileSelect.dataset.index = String(count);

        typeFileSelect.onchange = (event: Event) => {
            const target = event.target as HTMLSelectElement;
            const index = Number(target.dataset.index);

            const hasPortada = metadatos.find(m => m.type === "Portada");

            if (!hasPortada) {
                metadatos[index].type = "Portada";
            }
        };

        let element = document.createElement("img");

        const file = metadatos[count];

        fileTypes.map(type => {
            if (file.type.includes(type.mime.extension)) {
                element.src = type.mime.category === "1" ? previewUrls[count].url : type.mime.icon;
                const option = createFileOption(type.description);
                typeFileSelect.appendChild(option);
            }
        });

        element.className = "file";

        const label = document.createElement("p");
        label.className = "file-name";
        label.textContent = file.name;

        const deleteBtn = document.createElement("button");
        deleteBtn.className = "delete-file-button";

        deleteBtn.onclick = () => {
            selectedFiles.splice(count, 1);
            previewUrls.splice(count, 1);
            metadatos.splice(count, 1);
            loadFilesOnContainer();
        };

        const deleteImg = document.createElement("img");
        deleteImg.src = "/icons/trash.svg";
        deleteImg.className = "delete-file-image"

        deleteBtn.appendChild(deleteImg);

        container.appendChild(element);
        container.appendChild(label);
        container.appendChild(typeFileSelect);
        container.appendChild(deleteBtn);

        imagesContainer.appendChild(container);
    }
};

/* ===================== EVENTS ===================== */

const handleDragOver = (event: DragEvent): void => {
    event.preventDefault();
    (event.currentTarget as HTMLElement).classList.add("dragover");
};

const handleDragLeave = (event: DragEvent): void => {
    event.preventDefault();
    (event.currentTarget as HTMLElement).classList.remove("dragover");
};

const handleDrop = (event: DragEvent): void => {
    event.preventDefault();
    (event.currentTarget as HTMLElement).classList.remove("dragover");

    if (event.dataTransfer?.files.length) {
        processFiles(event.dataTransfer.files);
    }
};

const handleFileUpload = (event: Event): void => {
    const target = event.target as HTMLInputElement;
    if (target.files?.length) {
        processFiles(target.files);
    }
};

const handleInputTitle = (event: Event): void => {
    proposalTitle = (event.target as HTMLInputElement).value;
};

const handleInputDescription = (event: Event): void => {
    proposalDescription = (event.target as HTMLInputElement).value;
};

const changeFilePage = (page: number) => {
    filePage = page;
}

const handleChangePageIndex = (indexPage: number) => {
    if (!proposalFiles)
        return;

    proposalFiles.innerHTML = "";
    filePage = indexPage;
    
    if (filePage === indexPage)
    {
        let startCount = 5 * filePage;
        let endCount = (filePage + 1) * 5;
        chargeFileList(startCount, endCount);
    }
}

const handleUploadFiles = async (event: Event): Promise<void> => {
    try
    {
        const requestBody = new FormData();

        if (selectedFiles.length < 1)
        {
            showToast("No hay archivos cargados.", "warning")
            return;
        }

        selectedFiles.forEach(file => {
            requestBody.append("proposal_documentation", file);
        });

        const res = await uploadInfo(`proposal/${projectId}`, token, requestBody);

        const jsonResult = await res.json();

        if (!res.ok)
        {
            requestBody.delete("proposal_documentation");
            showToast(jsonResult.message, "warning");
            return
        }
            
        showToast("Archivos cargados correctamente.", "success");

        location.reload();
    } catch (e)
    {
        showToast("Error al enviar los documentos. Informe a soporte.", "error");
    }
}

(async () => {
    document.title = `Proyecto ${projectId}`;
    let startCount = 5 * (filePage - 1);
    let endCount = filePage * 5;
    
    const proposalInfoRow = await getInfo(`proposal/${projectId}`, token);
    const proposalMembersRow = await getInfo(`proposal/proposal-users/${projectId}`, token);

    const proposalFilesRow = await getInfo(`proposal/proposal-files/${projectId}`, token);

    const data = await getInfo("file-tipes", token)
    
    if (!proposalInfoRow.ok || !proposalMembersRow.ok) {
        return
    }

    const dataInfoJson = await proposalInfoRow.json();
    const dataMembersJson = await proposalMembersRow.json();
    const filesJson = await proposalFilesRow.json();
    let jsonData = await data.json() || [];

    fileTypes = jsonData["data"] || [];
    proposalInfo = dataInfoJson["data"];
    membersInfo = dataMembersJson["data"];
    filesInfo = filesJson["data"];

    totalPages = Math.ceil(filesInfo.length / 5);

    proposalTitleElement!.textContent = proposalInfo.title;
    proposalDescriptionElement!.textContent = proposalInfo.description;

    const userMembersTable = document.getElementById("user-members-body");

    membersInfo.map((member: UserMemberInterface) => {
        let rowMember = userMemberRow(member);
        userMembersTable?.appendChild(rowMember);
    });

    chargeFileList(startCount, endCount);

    pageIndexList("file-pagination", totalPages, handleChangePageIndex)
})();

/* ===================== GLOBAL ===================== */

declare global {
    interface Window {
        handleChangePageIndex: (numberPage: number) => void;
        changeFilePage: (page: number) => void;
        handleUploadFiles: (event: Event) => void;
        handleSendProposal: (event: Event) => void;
        handleInputTitle: (event: Event) => void;
        handleInputDescription: (event: Event) => void;
        handleFileUpload: (event: Event) => void;
        handleDrop: (event: DragEvent) => void;
        handleDragOver: (event: DragEvent) => void;
        handleDragLeave: (event: DragEvent) => void;
    }
}

window.handleInputTitle = handleInputTitle;
window.handleInputDescription = handleInputDescription;
window.handleFileUpload = handleFileUpload;
window.handleDrop = handleDrop;
window.handleDragOver = handleDragOver;
window.handleDragLeave = handleDragLeave;
window.handleUploadFiles = handleUploadFiles;
window.changeFilePage = changeFilePage;
window.handleChangePageIndex = handleChangePageIndex;