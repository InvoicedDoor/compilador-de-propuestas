import { cardComponent } from "../components/card.js";
import { getInfo } from "../functions/apiConnection.js";
import { verifyAuth } from "../functions/verifyAuth.js";

/* ===================== AUTH ===================== */

const token: string = localStorage.getItem("token") ?? "";

if (!token) {
    window.location.href = "/html/login.html";
}

(async () => {
    await verifyAuth(token);
})();
/* ===================== DOM ===================== */

const cardsContainer = document.getElementById("cards-container");

if (!cardsContainer) {
    throw new Error("cards-container no existe en el DOM");
}

/* ===================== TYPES ===================== */

interface CardData {
    id: number
    title: string;
    description: string;
    source: {
        source: string;
    };
}

interface ApiResponse<T> {
    data: T;
    message: string
}

function getProposalInfo(cardId: number) {
    window.location.href = "/project/" + cardId;
}

/* ===================== DATA ===================== */
(async () => {
    const response: Response = await getInfo("proposal", token);
    const dataJson: ApiResponse<CardData[]> = await response.json();

    // Limpia el contenedor
    cardsContainer.replaceChildren();

    if (!response.ok && dataJson.message !== "") {
        {
            const h3 = document.createElement("h3");

            h3.textContent = dataJson.message;
            cardsContainer.appendChild(h3);
            return;
        }
    }

    const cards = dataJson.data ?? [];

    cards.forEach((card: CardData) => {
        const cardElement = cardComponent(
            card.title,
            card.description,
            card.source.source,
            () => getProposalInfo(card.id)
        );

        cardsContainer.appendChild(cardElement);
    });

})();