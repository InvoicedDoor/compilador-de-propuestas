import { auth } from "../functions/apiConnection.js"
import { showToast } from "../components/notifications.js";

let mail = "";
let password = "";

const handleInputMail = (event) => {
    event.preventDefault();
    mail = event.target.value;
}

const handleInputPassword = (event) => {
    event.preventDefault();
    password = event.target.value;
}

const handleLogin = async (event) => {
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


window.handleInputMail = handleInputMail;
window.handleInputPassword = handleInputPassword;
window.handleLogin = handleLogin;