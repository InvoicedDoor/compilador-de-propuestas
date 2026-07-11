/*<div class="card">
    <div class="image-container">
        <img class="project-main-image" src="" alt="">
    </div>
    <div class="project-data">
        <div class="project-title">
            <h3 id="proposal-title">Titulo del proyecto</h3>
        </div>
        <div class="project-description">
            <p id="proposal-description">Proyecto de renovación de conceptos.</p>
        </div>
    </div>
    <div class="card-footer">
        <button class="edit-card-button">Editar</button>
        <button class="delete-card-button">Borrar</button>
    </div>
</div>*/

export const cardComponent = (titleContent: string, descriptionContent: string, imageSrc: string, onclick: () => void) => {
    const cardContainer = document.createElement("div");
    cardContainer.className = "card";
    cardContainer.onclick = onclick;

    const cardImageContainer = document.createElement("div");
    cardImageContainer.className = "image-container";
    
    const cardImage = document.createElement("img");
    cardImage.className = "project-main-image";
    cardImage.src = imageSrc ?? "/icons/file.svg";

    const informationContainer = document.createElement("div");
    informationContainer.className = "project-data";

    const titleContainer = document.createElement("div");
    titleContainer.className = "project-title";
    const title = document.createElement("h3");
    title.textContent = titleContent;
    
    const descriptionContainer = document.createElement("div");
    descriptionContainer.className = "project-description";
    const description = document.createElement("p");
    description.textContent = descriptionContent;

    const cardFooter = document.createElement("div");
    cardFooter.className = "card-footer";
    const buttonEdit = document.createElement("div");
    buttonEdit.className = "edit-card-button";
    buttonEdit.textContent = "Editar";
    const buttonDelete = document.createElement("div");
    buttonDelete.className = "delete-card-button";
    buttonDelete.textContent = "Borrar";
    cardFooter.appendChild(buttonEdit);
    cardFooter.appendChild(buttonDelete);

    titleContainer.appendChild(title);
    descriptionContainer.appendChild(description);
    informationContainer.appendChild(titleContainer);
    informationContainer.appendChild(descriptionContainer);
    cardImageContainer.appendChild(cardImage);
    cardContainer.appendChild(cardImageContainer);
    cardContainer.appendChild(informationContainer);
    cardContainer.appendChild(cardFooter);

    return cardContainer;
}