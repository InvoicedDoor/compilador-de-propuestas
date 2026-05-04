var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { auth } from "../functions/apiConnection.js";
import { showToast } from "../components/notifications.js";
let mail = "";
let password = "";
const handleInputMail = (event) => {
    event.preventDefault();
    const target = event.target;
    mail = target.value;
};
const handleInputPassword = (event) => {
    event.preventDefault();
    const target = event.target;
    password = target.value;
};
const handleLogin = (event) => __awaiter(void 0, void 0, void 0, function* () {
    event.preventDefault();
    try {
        const body = {
            mail: mail,
            password: password
        };
        const res = yield auth(body);
        const result = yield res.json();
        if (!res.ok) {
            showToast(result.message, "error");
            return;
        }
        localStorage.setItem("token", result.data);
        showToast("Bienvenido.");
        setTimeout(() => {
            window.location.href = "/";
        }, 1000);
    }
    catch (error) {
        showToast("Error de conexión.", "error");
        console.error(error);
    }
});
window.handleInputMail = handleInputMail;
window.handleInputPassword = handleInputPassword;
window.handleLogin = handleLogin;
