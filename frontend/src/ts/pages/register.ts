import { auth } from "../functions/apiConnection.js";
import { showToast } from "../components/notifications.js";

const requestBody = {

    name: "",
    lastname: "",
    mail: "",
    password: "",
    confirmPassword: ""
} 

const handleInput = (event: Event) => {
    event.preventDefault();
    try
    {
        const target = event.target as HTMLInputElement;

        switch (target.id)
        {
            case "name":
                requestBody.name = target.value;
            case "lastname":
                requestBody.lastname = target.value;
            case "mail":
                requestBody.mail = target.value;
            case "password":
                requestBody.password = target.value;
            case "confirm-password":
                requestBody.confirmPassword = target.value;
            _:
                return;
        }
    } catch (e)
    {
        console.log("Error al ingresar los valores");
    }
}

const handleLogin = async (event: any) => {
    event.preventDefault();

    try {

        const body = requestBody

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
        handleInput: (event: Event) => void;
        handleRegister: (event: Event) => void;
    }
}

window.handleInput = handleInput;
window.handleRegister = handleLogin;