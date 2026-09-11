export const pageIndexList = (
    elementId: string,
    initialPage: number,
    finalPage: number,
    currentPage: number,
    totalElementsByPage: number,
    handleChangePageIndex: (elementCount: number) => void,
    handleChangeLeftIndex: () => void,
    handleChangeRightIndex: () => void
) => {

    const baseElement = document.getElementById(elementId);

    if (!baseElement)
        return;

    const orderedList = document.createElement("ol");

    const leftArrowImage = document.createElement("i");
    leftArrowImage.className = "left-arrow-image";

    const rightArrowImage = document.createElement("i");
    rightArrowImage.className = "right-arrow-image";


    // LEFT ARROW
    const leftArrow = document.createElement("li");

    leftArrow.className = "page-index";
    leftArrow.id = "left-arrow";
    leftArrow.onclick = handleChangeLeftIndex;

    leftArrow.appendChild(leftArrowImage);
    orderedList.appendChild(leftArrow);


    // PAGE INDEXES
    for (
        let elementCount = initialPage;
        elementCount <= finalPage;
        elementCount++
    ) {

        const pageIndex = document.createElement("li");
        const paragraphElement = document.createElement("p");

        pageIndex.className = "page-index";

        paragraphElement.textContent =
            elementCount.toString();

        pageIndex.appendChild(paragraphElement);

        pageIndex.onclick = () =>
            handleChangePageIndex(elementCount);


        if (elementCount === currentPage) {
            pageIndex.style.backgroundColor = "#2d2d2d";
        }

        orderedList.appendChild(pageIndex);
    }


    // RIGHT ARROW
    const rightArrow = document.createElement("li");

    rightArrow.className = "page-index";
    rightArrow.id = "right-arrow";
    rightArrow.onclick = handleChangeRightIndex;

    rightArrow.appendChild(rightArrowImage);
    orderedList.appendChild(rightArrow);


    // REPLACE PAGINATION
    baseElement.innerHTML = "";
    baseElement.appendChild(orderedList);
};

export const validatePaginationToHiddeArrows = (indexPage: number, totalPages: number) => {
    const leftArrow = document.getElementById("left-arrow");
    if (!leftArrow)
        return;

    const rightArrow = document.getElementById("right-arrow");
    if (!rightArrow)
        return

    if (totalPages === 0)
    {
        leftArrow.hidden = true;
        rightArrow.hidden = true;
        return;
    }

    switch (indexPage) {
        case 1:
            leftArrow.hidden = true;
            rightArrow.hidden = false;
            break;
        case totalPages:
            leftArrow.hidden = false;
            rightArrow.hidden = true;
            break;
        default:
            leftArrow.hidden = false;
            rightArrow.hidden = false;
            break;
    }
}