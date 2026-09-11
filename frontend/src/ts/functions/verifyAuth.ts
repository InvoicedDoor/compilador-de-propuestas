import { getInfo } from "./apiConnection.js";
import { userStore } from '../functions/userStorage.js'

export const verifyAuth = async (token: string) =>
{
    const res = await getInfo("auth", token);

    if (!res.ok)
    {
        localStorage.clear()
        window.location.href = "/html/login.html";
    }

    const jsonResponse = await res.json();

    const jsonData = jsonResponse["data"];

    userStore.name = jsonData["name"];    
    userStore.role = jsonData["rol"];    
}