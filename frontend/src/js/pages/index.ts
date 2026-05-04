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
}) ();
/* ===================== DOM ===================== */

const cardsContainer = document.getElementById("cards-container");

if (!cardsContainer) {
    throw new Error("cards-container no existe en el DOM");
}

/* ===================== TYPES ===================== */

interface CardData {
    title: string;
    description: string;
    source: {
        source: string;
    };
}

interface ApiResponse<T> {
    data: T;
}

/* ===================== DATA ===================== */
(async () => {
    const response: Response = await getInfo("proposal", token);
    const dataJson: ApiResponse<CardData[]> = await response.json();

    if (response.ok) {
        const cards = dataJson.data ?? [];

        if (!cardsContainer.hasChildNodes() && cards.length > 0) {

            cards.forEach((card: CardData) => {
                const cardElement = cardComponent(
                    card.title,
                    card.description,
                    card.source.source
                );

                cardsContainer.appendChild(cardElement);
            });

        }
    }
}) ();