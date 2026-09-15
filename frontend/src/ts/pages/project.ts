
import { projectFileRow } from "../components/element/projectFileRow.js";
import { userMemberRow } from "../components/element/userMemberRow.js";
import { getInfo, uploadInfo, deleteInfo } from "../functions/apiConnection.js";
import { verifyAuth } from "../functions/verifyAuth.js";
import { createFileOption } from "../components/element/fileTypeButton.js";
import { FileInterface, Metadata, Preview } from "../interfaces/file.interface.js";
import { UserMemberInterface } from "../interfaces/userMember.interface.js";
import FileTypeModel from "../models/fileType.model.js";
import { showToast } from "../components/modal/notifications.js";
import { pageIndexList, validatePaginationToHiddeArrows } from "../components/element/pageIndexList.js";
import projectInfoStore from "../storages/projectInfoStorage.js";
import { leftBarComponent } from "../components/section/leftBar.js";

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
let projectInfo: any = null;
let membersInfo: any = [];
let filesInfo: Array<FileInterface> = [];
const projectTitleElement = document.getElementById("project-title");
const projectDescriptionElement = document.getElementById("project-description");
const projectFiles = document.getElementById("file-list-element");

const selectedFiles: File[] = [];
const metadatos: Metadata[] = [];
const previewUrls: Preview[] = [];


let projectTitle: string = "";
let projectDescription: string = "";
const FILES_PER_PAGE = 5;
const VISIBLE_PAGES = 4;
let temporalId: number = 1;
let filePage = 1;
let totalPages = 1;
let firstPage = 1;
let finalPage = 5;

/* ===================== RENDER ===================== */
const processFiles = (files: FileList): void => {
    const imagesContainer = document.getElementById("show_files_container") as HTMLElement;

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

const cleanFilesFromContainer = () => {
    if (!projectFiles)
        return;
    projectFiles.innerHTML = "";
}

const chargeFileList = async (startCount: number, endCount: number) => {
    await getFiles();

    if (filesInfo.length === 0)
    {
        const noInfoContainer = document.createElement("div");
        noInfoContainer.className = "files-list";
        const noInfo = document.createElement("h3");
        noInfo.textContent = "No hay archivos para mostrar."
        noInfoContainer.appendChild(noInfo);
        return noInfoContainer;
    }
        
    const orederedList = document.createElement("ol");
    orederedList.className = "files-list";
    
    for (let pageCount = startCount; pageCount < endCount; pageCount++)
    {
        if (pageCount > endCount || pageCount >= filesInfo.length)
        {
            break;
        }

        let rowFile = projectFileRow(projectId, filesInfo[pageCount], handleDeleteFile);

        orederedList.appendChild(rowFile);
    }

    return orederedList;
}

const getFiles = async () => {
    const projectFilesRow = await getInfo(`project/project-files/${projectId}`, token);
    const filesJson = await projectFilesRow.json();
    filesInfo = filesJson["data"];
}

const loadFilesOnContainer = (): void => {
    const imagesContainer = document.getElementById("show_files_container") as HTMLElement;
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

export const handleDragOver = (event: DragEvent): void => {
    event.preventDefault();
    (event.currentTarget as HTMLElement).classList.add("dragover");
};

export const handleDragLeave = (event: DragEvent): void => {
    event.preventDefault();
    (event.currentTarget as HTMLElement).classList.remove("dragover");
};

export const handleDrop = (event: DragEvent): void => {
    event.preventDefault();
    (event.currentTarget as HTMLElement).classList.remove("dragover");

    if (event.dataTransfer?.files.length) {
        processFiles(event.dataTransfer.files);
    }
};

export const handleFileUpload = (event: Event): void => {
    const target = event.target as HTMLInputElement;
    if (target.files?.length) {
        processFiles(target.files);
    }
};

const handleInputTitle = (event: Event): void => {
    projectTitle = (event.target as HTMLInputElement).value;
};

const handleInputDescription = (event: Event): void => {
    projectDescription = (event.target as HTMLInputElement).value;
};

const changeFilePage = (page: number) => {
    filePage = page;
}

const handleChangePageIndex = async (indexPage: number) => {

    if (!projectFiles)
        return;

    if (indexPage < 1 || indexPage > totalPages)
        return;

    filePage = indexPage;
    
    // Donde empieza el array de elementos
    const startCount =
    FILES_PER_PAGE * (filePage - 1);
    
    // Donde termina el array de elementos
    const endCount =
        filePage * FILES_PER_PAGE;

    const orderedList =
        await chargeFileList(
            startCount,
            endCount
        );

    if (!orderedList)
        return;

    projectFiles.innerHTML = "";
    projectFiles.appendChild(orderedList);

    finalPage = Math.min(
        firstPage + VISIBLE_PAGES,
        totalPages
    );

    pageIndexList(
        "file-pagination",
        firstPage,
        finalPage,
        filePage,
        endCount,
        handleChangePageIndex,
        handleChangeLeftIndex,
        handleChangeRightIndex
    );

    validatePaginationToHiddeArrows(
        filePage,
        totalPages
    );
};

const handleChangeRightIndex = async () => {

    if (filePage > totalPages)
        return;

    filePage++;

    // Solo mover la ventana cuando
    // salimos de ella por la derecha
    if ((firstPage + VISIBLE_PAGES) < totalPages)
        firstPage++;
    
    await handleChangePageIndex(filePage);
};

const handleChangeLeftIndex = async () => {
    if (filePage < 1)
        return;
    
    filePage--;
    
    // Solo mover la ventana cuando
    // salimos de ella por la izquierda
    if (firstPage > 1) {
        firstPage--;
    }
    
    await handleChangePageIndex(filePage);
};

const handleDeleteFile = async (projectId: number, fileId: number) => {
    const queryStringArgs = [
        {
            key: "project", 
            value: projectId
        }, 
        {
            key: "file", 
            value: fileId
        }
    ]
    const res = await deleteInfo("project/project-files", token, null, queryStringArgs)

    const resJson = await res.json()
    if (!res.ok)
    {
        showToast(resJson.message, "warning");
        return;
    }
    showToast(resJson.message, "success");
    
    await getFiles();
    
    totalPages = Math.ceil(filesInfo.length / FILES_PER_PAGE);

    if (filePage < 1)
        return;
    
    
    // Solo mover la ventana cuando
    // salimos de ella por la izquierda
    if (filePage > totalPages) {
        filePage--;
    }

    if (firstPage > 1) {
        firstPage--;
    }

    finalPage = Math.min(
        firstPage + VISIBLE_PAGES,
        totalPages
    );
        
    cleanFilesFromContainer();

    await handleChangePageIndex(filePage);
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
            requestBody.append("project_documentation", file);
        });

        const res = await uploadInfo(`project/${projectId}`, token, requestBody);

        const jsonResult = await res.json();

        if (!res.ok)
        {
            requestBody.delete("project_documentation");
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
    let startCount = FILES_PER_PAGE * (filePage - 1);
    let endCount = filePage * FILES_PER_PAGE;
    
    const projectInfoRow = await getInfo(`project/${projectId}`, token);
    const projectMembersRow = await getInfo(`project/project-users/${projectId}`, token);
    await getFiles();

    const data = await getInfo("file-tipes", token)
    
    const dataInfoJson = await projectInfoRow.json();
    const dataMembersJson = await projectMembersRow.json();
    let jsonData = await data.json() || [];

    if (!projectInfoRow.ok || !projectMembersRow.ok) {
        showToast(dataInfoJson.message, "warning");
        showToast(dataMembersJson.message, "warning");
        return
    }

    fileTypes = jsonData["data"] || [];
    projectInfo = dataInfoJson["data"];
    projectInfoStore.projectInfoActions.setInfo(projectInfo);

    console.log(projectInfoStore.store.id)
    membersInfo = dataMembersJson["data"];

    totalPages = Math.ceil(filesInfo.length / FILES_PER_PAGE);

    firstPage = 1;

    finalPage = Math.min(
        firstPage + VISIBLE_PAGES,
        totalPages
    );
    projectTitleElement!.textContent = projectInfo.title;
    projectDescriptionElement!.textContent = projectInfo.description;

    const userMembersTable = document.getElementById("user-members-body");

    membersInfo.map((member: UserMemberInterface) => {
        let rowMember = userMemberRow(member);
        let rowMemberCopy = userMemberRow(member);
        userMembersTable?.appendChild(rowMember);
        userMembersTable?.appendChild(rowMemberCopy);
    });

    const orderedList = await chargeFileList(startCount, endCount);

    pageIndexList(
        "file-pagination",
        firstPage,
        finalPage,
        filePage,
        endCount,
        handleChangePageIndex,
        handleChangeLeftIndex,
        handleChangeRightIndex
    );
    validatePaginationToHiddeArrows(filePage, totalPages);
    projectFiles?.appendChild(orderedList || document.createElement("ol"));
    leftBarComponent();
})();

/* ===================== GLOBAL ===================== */

declare global {
    interface Window {
        handleChangePageIndex: (numberPage: number) => void;
        changeFilePage: (page: number) => void;
        handleUploadFiles: (event: Event) => void;
        handleSendProject: (event: Event) => void;
        handleInputTitle: (event: Event) => void;
        handleInputDescription: (event: Event) => void;
    }
}

window.handleInputTitle = handleInputTitle;
window.handleInputDescription = handleInputDescription;
window.handleUploadFiles = handleUploadFiles;
window.changeFilePage = changeFilePage;
window.handleChangePageIndex = handleChangePageIndex;