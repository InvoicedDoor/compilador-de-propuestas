import { getInfo } from "../functions/apiConnection";
const token = "";
export const fileTypeButton = () => {
    const fileTypes = getInfo("file-types", token);
};
