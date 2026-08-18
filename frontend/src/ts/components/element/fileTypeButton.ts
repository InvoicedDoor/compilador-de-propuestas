export const createFileOption = (fileType: string) => {
    const option = document.createElement("option");
    option.text = fileType;
    option.value = fileType;

    return option;
}