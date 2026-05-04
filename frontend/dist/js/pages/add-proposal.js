var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var _a;
import { verifyAuth } from "../functions/verifyAuth.js";
import { uploadInfo } from "../functions/apiConnection.js";
import { showToast } from "../components/notifications.js";
/* ===================== AUTH ===================== */
const token = (_a = localStorage.getItem("token")) !== null && _a !== void 0 ? _a : "";
if (!token) {
    window.location.href = "/html/login.html";
}
verifyAuth(token);
/* ===================== STATE ===================== */
const fileTypes = [];
const selectedFiles = [];
const metadatos = [];
const previewUrls = [];
const imagesContainer = document.getElementById("show_files_container");
let proposalTitle = "";
let proposalDescription = "";
let temporalId = 1;
/* ===================== FILES ===================== */
const processFiles = (files) => {
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const exists = selectedFiles.find(f => f.name === file.name &&
            f.size === file.size &&
            f.lastModified === file.lastModified);
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
const loadFilesOnContainer = () => {
    imagesContainer.innerHTML = "";
    for (let count = 0; count < previewUrls.length; count++) {
        const container = document.createElement("div");
        container.className = "file-item";
        const typeFileSelect = document.createElement("select");
        typeFileSelect.className = "type-file-select";
        typeFileSelect.dataset.index = String(count);
        typeFileSelect.onchange = (event) => {
            const target = event.target;
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
        }
        else if (mime === "application/pdf") {
            element.src = "/icons/pdf.svg";
            typeFileSelect.appendChild(createFileOption("Documento"));
        }
        else if (mime.includes("spreadsheet") || file.name.endsWith(".xlsx")) {
            element.src = "/icons/excel.svg";
            typeFileSelect.appendChild(createFileOption("Cálculo"));
        }
        else if (mime.includes("word") || file.name.endsWith(".docx")) {
            element.src = "/icons/word.svg";
            typeFileSelect.appendChild(createFileOption("Documento"));
        }
        else {
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
        deleteImg.className = "delete-file-image";
        deleteBtn.appendChild(deleteImg);
        container.appendChild(element);
        container.appendChild(label);
        container.appendChild(typeFileSelect);
        container.appendChild(deleteBtn);
        imagesContainer.appendChild(container);
    }
};
/* ===================== HELPERS ===================== */
const createFileOption = (fileType) => {
    const option = document.createElement("option");
    option.text = fileType;
    option.value = fileType;
    return option;
};
/* ===================== EVENTS ===================== */
const handleDragOver = (event) => {
    event.preventDefault();
    event.currentTarget.classList.add("dragover");
};
const handleDragLeave = (event) => {
    event.preventDefault();
    event.currentTarget.classList.remove("dragover");
};
const handleDrop = (event) => {
    var _a;
    event.preventDefault();
    event.currentTarget.classList.remove("dragover");
    if ((_a = event.dataTransfer) === null || _a === void 0 ? void 0 : _a.files.length) {
        processFiles(event.dataTransfer.files);
    }
};
const handleFileUpload = (event) => {
    var _a;
    const target = event.target;
    if ((_a = target.files) === null || _a === void 0 ? void 0 : _a.length) {
        processFiles(target.files);
    }
};
const handleInputTitle = (event) => {
    proposalTitle = event.target.value;
};
const handleInputDescription = (event) => {
    proposalDescription = event.target.value;
};
/* ===================== SUBMIT ===================== */
const handleSendProposal = (event) => __awaiter(void 0, void 0, void 0, function* () {
    var _a;
    event.preventDefault();
    try {
        const body = new FormData();
        body.append("proposal_title", proposalTitle);
        body.append("proposal_description", proposalDescription);
        selectedFiles.forEach(file => {
            body.append("proposal_documentation", file);
        });
        const token = (_a = localStorage.getItem("token")) !== null && _a !== void 0 ? _a : "";
        const res = yield uploadInfo("proposal/", token, body);
        const result = yield res.json();
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
    }
    catch (error) {
        showToast("Error inesperado.", "error");
        console.error(error);
    }
});
window.handleSendProposal = handleSendProposal;
window.handleInputTitle = handleInputTitle;
window.handleInputDescription = handleInputDescription;
window.handleFileUpload = handleFileUpload;
window.handleDrop = handleDrop;
window.handleDragOver = handleDragOver;
window.handleDragLeave = handleDragLeave;
