interface ModalAddProjectElementsInterface {
    content: HTMLElement,
    closeModal: EventListener
}

export function modalAddProjectElements(props: ModalAddProjectElementsInterface) {
    const overlay = document.createElement("div");

    overlay.className = "modal-overlay";
    overlay.id = "modal-overlay";

    overlay.innerHTML = `
        <div class="window-modal">
            <p>Hola</p>
        </div>
    `;

    overlay.querySelector(".button-close")
        ?.addEventListener("click", props.closeModal);

    return overlay;
}