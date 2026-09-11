import { register } from "../functions/apiConnection.js";
import { showToast } from "../components/modal/notifications.js";

const requestBody: Record<string, string> = {
  name: "",
  first_lastname: "",
  second_lastname: "",
  mail: "",
  password: "",
  confirm_password: ""
}

const handleInput = (event: Event) => {
    event.preventDefault();
    try
    {
        const target = event.target as HTMLInputElement;

        requestBody[target.id] = target.value;
    } catch (e)
    {
        showToast("Error al registrar al usuario. Consulte al administrador de la aplicación.", "warning");
    }
}

const handleRegister = async (event: any) => {
    event.preventDefault();

    try {

        const res = await register("register", requestBody);

        if (!res.ok) {
            showToast("No se pudo registrar al usuario.", "warning");
            return;
        }

        showToast("Registro realizado correctamente.");
        setTimeout(() => {
            window.location.href = "/html/login.html";
        }, 1000);
    } catch (error) {
        showToast("Error de conexión.", "error");
        console.error(error);
    }


}

declare global {
    interface Window {
        handleInput: (event: Event) => void;
        handleRegister: (event: Event) => void;
    }
}

window.handleInput = handleInput;
window.handleRegister = handleRegister;