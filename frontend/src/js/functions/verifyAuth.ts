import { getInfo } from "./apiConnection.js";

export const verifyAuth = async (token: string) =>
{
    const res = await getInfo("auth", token);

    if (!res.ok)
    {
        localStorage.clear()
        window.location.href = "/html/login.html";
    }
}