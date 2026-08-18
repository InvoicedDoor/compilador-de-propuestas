import { PositionOptions } from "../../interfaces/positionElementInterface";

export const positionElement = (
    reference: HTMLElement,
    element: HTMLElement,
    options: PositionOptions = {}
) => {

    const {
        placement = "bottom",
        offset = 8
    } = options;

    const rect = reference.getBoundingClientRect();

    element.style.position = "absolute";

    switch (placement) {

        case "bottom":
            element.style.left = `${rect.left + window.scrollX}px`;
            element.style.top = `${rect.bottom + window.scrollY + offset}px`;
            break;

        case "top":
            element.style.left = `${rect.left + window.scrollX}px`;
            element.style.top =
                `${rect.top + window.scrollY - element.offsetHeight - offset}px`;
            break;

        case "left":
            element.style.left =
                `${rect.left + window.scrollX - element.offsetWidth - offset}px`;
            element.style.top = `${rect.top + window.scrollY}px`;
            break;

        case "right":
            element.style.left =
                `${rect.right + window.scrollX + offset}px`;
            element.style.top = `${rect.top + window.scrollY}px`;
            break;
    }
};