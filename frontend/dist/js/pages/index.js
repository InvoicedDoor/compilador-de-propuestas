var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var _a;
import { cardComponent } from "../components/card.js";
import { getInfo } from "../functions/apiConnection.js";
import { verifyAuth } from "../functions/verifyAuth.js";
/* ===================== AUTH ===================== */
const token = (_a = localStorage.getItem("token")) !== null && _a !== void 0 ? _a : "";
if (!token) {
    window.location.href = "/html/login.html";
}
(() => __awaiter(void 0, void 0, void 0, function* () {
    yield verifyAuth(token);
}))();
/* ===================== DOM ===================== */
const cardsContainer = document.getElementById("cards-container");
if (!cardsContainer) {
    throw new Error("cards-container no existe en el DOM");
}
/* ===================== DATA ===================== */
(() => __awaiter(void 0, void 0, void 0, function* () {
    var _a;
    const response = yield getInfo("proposal", token);
    const dataJson = yield response.json();
    if (response.ok) {
        const cards = (_a = dataJson.data) !== null && _a !== void 0 ? _a : [];
        if (!cardsContainer.hasChildNodes() && cards.length > 0) {
            cards.forEach((card) => {
                const cardElement = cardComponent(card.title, card.description, card.source.source);
                cardsContainer.appendChild(cardElement);
            });
        }
    }
}))();
