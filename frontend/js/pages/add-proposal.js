import { verifyAuth } from "../functions/verifyAuth.js";

const token = localStorage.getItem("token");

verifyAuth(token);

if (!token) {
    window.location.href = "/html/login.html";
}

import { getInfo, uploadInfo, modifyInfo } from "../functions/apiConnection.js"
import { showToast } from "../components/notifications.js";

const selectedFiles = [];
const previewUrls = [];
const imagesContainer = document.getElementById("show_files_container");
let proposalTitle = "";
let proposalDescription = "";
let temporalId = 1;

const processFiles = (files) => {

    for (let i = 0; i < files.length; i++) {
        const file = files[i];

        if (selectedFiles.find(f =>
            f.name === file.name &&
            f.size === file.size &&
            f.lastModified === file.lastModified
        )) {
            alert("Archivo ya existente.");
            continue; // mejor que return
        }

        selectedFiles.push(file);
        previewUrls.push({
            id: temporalId,
            url: URL.createObjectURL(file),
            type: file.type,
            name: file.name
        });

        temporalId++;
    }

    loadFilesOnContainer();

    imagesContainer.classList.replace("no-show-files", "show-files");
};

const loadFilesOnContainer = () => {
    imagesContainer.innerHTML = "";

    previewUrls.forEach(file => {
        const container = document.createElement("div");
        container.className = "file-item";

        let element;

        if (file.type.startsWith("image/")) {
            element = document.createElement("img");
            element.src = file.url;
        }
        else if (file.type === "application/pdf") {
            element = document.createElement("img");
            element.src = "/icons/pdf.svg"; // ruta a tu ícono
        }
        else if (file.type.includes("spreadsheet") || file.name.endsWith(".xlsx")) {
            element = document.createElement("img");
            element.src = "/icons/excel.svg";
        }
        else if (file.type.includes("word") || file.name.endsWith(".docx")) {
            element = document.createElement("img");
            element.src = "/icons/word.svg";
        }
        else {
            element = document.createElement("img");
            element.src = "/icons/file.svg";
        }

        element.className = "file";

        const label = document.createElement("p");
        label.className = "file-name";
        label.textContent = file.name;

        container.appendChild(element);
        container.appendChild(label);

        imagesContainer.appendChild(container);
    });
};

const handleDragOver = (event) => {
    event.preventDefault();
    event.currentTarget.classList.add("dragover");
};

const handleDragLeave = (event) => {
    event.preventDefault();
    event.currentTarget.classList.remove("dragover");
};

const handleDrop = (event) => {
    event.preventDefault();

    event.currentTarget.classList.remove("dragover");

    if (event.dataTransfer?.files.length) {
        processFiles(event.dataTransfer.files);
    }
};

const handleFileUpload = (event) => {
    const target = event.target;
    if (target.files?.length) {
        processFiles(target.files);
    }
}

const handleInputTitle = (event) => {
    proposalTitle = event.target.value;
}

const handleInputDescription = (event) => {
    proposalDescription = event.target.value
}

const handleSendProposal = async (event) => {
    event.preventDefault();
    try {

        const body = new FormData();
        body.append("proposal_title", proposalTitle)
        body.append("proposal_description", proposalDescription)
        selectedFiles.forEach(file => {
            body.append("proposal_documentation", file)
        });

        const token = localStorage.getItem("token");
        const res = await uploadInfo("proposal/", token, body);

        const result = await res.json()

        if (!res.ok) {
            showToast(result["message"], "warning")
            return;
        }


        showToast(result["message"])

        selectedFiles.pop();
        previewUrls.pop();
        imagesContainer.classList.replace("show-files", "no-show-files");
        proposalTitle = "";
        proposalDescription = "";
        temporalId = 1;
    } catch (error) {
        showToast("Error inesperado.", "error")
        console.error(error)
    }
}

// Exponer al scope global
window.handleSendProposal = handleSendProposal;
window.handleInputTitle = handleInputTitle;
window.handleInputDescription = handleInputDescription;
window.handleFileUpload = handleFileUpload;
window.handleDrop = handleDrop;
window.handleDragOver = handleDragOver;
window.handleDragLeave = handleDragLeave;
window.showToast = showToast;