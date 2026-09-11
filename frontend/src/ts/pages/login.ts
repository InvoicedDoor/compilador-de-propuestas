import { auth } from "../functions/apiConnection.js";
import { showToast } from "../components/modal/notifications.js";
import { userStore } from '../functions/userStorage.js'

const requestBody: Record<string, string> = {
    mail: "",
    password: ""
}

const handleInput = (event: Event) => {
    event.preventDefault();
    try
    {
        const target = event.target as HTMLInputElement;
        requestBody[String(target.id)] = target.value;
    } catch (e)
    {
        showToast("Error al iniciar la sesión. Consulte al administrador de la aplicación.", "warning");

    }
}

const handleLogin = async (event: any) => {
    event.preventDefault();

    try {

        const body = requestBody;

        const res = await auth(body);

        const result = await res.json();

        if (!res.ok) {
            showToast(result.message, "error");
            return;
        }


        localStorage.setItem("token", result.data["payload"])

        const user = result.data["user"];

        showToast(`Bienvenido. ${user.name}`);
        userStore.name = user.name;
        userStore.role = user.rol;

        setTimeout(() => {
            window.location.href = "/";
        }, 500);
    } catch (error) {
        showToast("Error de conexión.", "error");
        console.error(error);
    }


}

declare global {
    interface Window {
        handleInput: (event: Event) => void;
        handleLogin: (event: Event) => void;
    }
}

window.handleInput = handleInput;
window.handleLogin = handleLogin;