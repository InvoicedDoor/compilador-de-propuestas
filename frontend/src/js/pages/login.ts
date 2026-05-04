import { auth } from "../functions/apiConnection.js";
import { showToast } from "../components/notifications.js";

let mail = "";
let password = "";

const handleInputMail = (event: Event) => {
    event.preventDefault();
    const target = event.target as HTMLInputElement;
    mail = target.value;
}

const handleInputPassword = (event: any) => {
    event.preventDefault();
    const target = event.target as HTMLInputElement;
    password = target.value;
}

const handleLogin = async (event: any) => {
    event.preventDefault();

    try {

        const body = {
            mail: mail,
            password: password
        }

        const res = await auth(body)

        const result = await res.json();

        if (!res.ok) {
            showToast(result.message, "error");
            return;
        }


        localStorage.setItem("token", result.data)

        showToast("Bienvenido.")

        setTimeout(() => {
            window.location.href = "/";
        }, 1000);
    } catch (error) {
        showToast("Error de conexión.", "error");
        console.error(error);
    }


}

declare global {
    interface Window {
        handleInputMail: (event: Event) => void;
        handleInputPassword: (event: Event) => void;
        handleLogin: (event: Event) => void;
    }
}

window.handleInputMail = handleInputMail;
window.handleInputPassword = handleInputPassword;
window.handleLogin = handleLogin;