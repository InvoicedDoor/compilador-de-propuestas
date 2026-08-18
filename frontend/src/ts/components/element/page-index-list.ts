export const pageIndexList = (elementId: string, pages: number, handleChangePageIndex: (elementCount: number) =>  void) => {
    const baseElement = document.getElementById(elementId);
    
    const orderedList = document.createElement("ol");
    
    const leftArrowImage = document.createElement("i");
    leftArrowImage.className = "left-arrow-image";

    const rightArrowImage = document.createElement("i");
    rightArrowImage.className = "right-arrow-image";

    const leftArrow = document.createElement("li");
    leftArrow.className = "page-index";
    leftArrow.appendChild(leftArrowImage);
    orderedList.appendChild(leftArrow);

    for (let elementCount = 0;  elementCount < pages; elementCount++)
    {
        const pageindex = document.createElement("li");
        pageindex.className = "page-index";
        const paragraphElement = document.createElement("p");
        paragraphElement.textContent = (elementCount + 1).toString();
        pageindex.appendChild(paragraphElement);
        pageindex.onclick = () => handleChangePageIndex(elementCount)
        orderedList.appendChild(pageindex);
    }

    const rightArrow = document.createElement("li");
    rightArrow.className = "page-index";
    rightArrow.appendChild(rightArrowImage);
    orderedList.appendChild(rightArrow);

    baseElement?.appendChild(orderedList);
}