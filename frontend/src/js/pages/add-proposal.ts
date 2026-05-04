import { verifyAuth } from "../functions/verifyAuth.js";
import { getInfo, uploadInfo, modifyInfo } from "../functions/apiConnection.js";
import { showToast } from "../components/notifications.js";

/* ===================== TIPOS ===================== */

type FileType = string | "Portada";

interface Metadata {
    id: number;
    type: FileType;
    name: string;
}

interface Preview {
    id: number;
    url: string;
}

/* ===================== AUTH ===================== */

const token: string = localStorage.getItem("token") ?? "";

if (!token) {
    window.location.href = "/html/login.html";
}

verifyAuth(token);

/* ===================== STATE ===================== */

const fileTypes: string[] = [];
const selectedFiles: File[] = [];
const metadatos: Metadata[] = [];
const previewUrls: Preview[] = [];

const imagesContainer = document.getElementById("show_files_container") as HTMLElement;

let proposalTitle: string = "";
let proposalDescription: string = "";
let temporalId: number = 1;

/* ===================== FILES ===================== */

const processFiles = (files: FileList): void => {

    for (let i = 0; i < files.length; i++) {
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
    }

    loadFilesOnContainer();

    imagesContainer.classList.replace("no-show-files", "show-files");
};

/* ===================== RENDER ===================== */

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
        const mime = typeof file.type === "string" ? file.type : "image/*";

        if (mime.startsWith("image/")) {
            element.src = previewUrls[count].url;

            typeFileSelect.appendChild(createFileOption("Portada"));
            typeFileSelect.appendChild(createFileOption("Imagen"));

        } else if (mime === "application/pdf") {
            element.src = "/icons/pdf.svg";
            typeFileSelect.appendChild(createFileOption("Documento"));

        } else if (mime.includes("spreadsheet") || file.name.endsWith(".xlsx")) {
            element.src = "/icons/excel.svg";
            typeFileSelect.appendChild(createFileOption("Cálculo"));

        } else if (mime.includes("word") || file.name.endsWith(".docx")) {
            element.src = "/icons/word.svg";
            typeFileSelect.appendChild(createFileOption("Documento"));

        } else {
            element.src = "/icons/file.svg";
            typeFileSelect.appendChild(createFileOption("Documento"));
        }

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

/* ===================== HELPERS ===================== */

const createFileOption = (fileType: string): HTMLOptionElement => {
    const option = document.createElement("option");
    option.text = fileType;
    option.value = fileType;
    return option;
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

/* ===================== SUBMIT ===================== */

const handleSendProposal = async (event: Event): Promise<void> => {
    event.preventDefault();

    try {
        const body = new FormData();

        body.append("proposal_title", proposalTitle);
        body.append("proposal_description", proposalDescription);

        selectedFiles.forEach(file => {
            body.append("proposal_documentation", file);
        });

        const token = localStorage.getItem("token") ?? "";
        const res = await uploadInfo("proposal/", token, body);
        const result = await res.json();

        if (!res.ok) {
            showToast(result.message, "warning");
            return;
        }

        showToast(result.message);

        selectedFiles.length = 0;
        previewUrls.length = 0;
        metadatos.length = 0;

        imagesContainer.classList.replace("show-files", "no-show-files");

        proposalTitle = "";
        proposalDescription = "";
        temporalId = 1;

    } catch (error) {
        showToast("Error inesperado.", "error");
        console.error(error);
    }
};

/* ===================== GLOBAL ===================== */

declare global {
    interface Window {
        handleSendProposal: (event: Event) => void;
        handleInputTitle: (event: Event) => void;
        handleInputDescription: (event: Event) => void;
        handleFileUpload: (event: Event) => void;
        handleDrop: (event: DragEvent) => void;
        handleDragOver: (event: DragEvent) => void;
        handleDragLeave: (event: DragEvent) => void;
    }
}

window.handleSendProposal = handleSendProposal;
window.handleInputTitle = handleInputTitle;
window.handleInputDescription = handleInputDescription;
window.handleFileUpload = handleFileUpload;
window.handleDrop = handleDrop;
window.handleDragOver = handleDragOver;
window.handleDragLeave = handleDragLeave;