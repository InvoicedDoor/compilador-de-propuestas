import { cardComponent } from "../components/card.js";
import { getInfo } from "../functions/apiConnection.js";
import { verifyAuth } from "../functions/verifyAuth.js";

const token = localStorage.getItem("token");

verifyAuth(token);

if (!token) {
    window.location.href = "/html/login.html";
}

const cardsContainer = document.getElementById("cards-container");
const data = await getInfo("proposal", token);
const dataJson = await data.json();

if (data.ok) {
    const cards = dataJson["data"] || [];
    // const cards = [
    //     {
    //         title: "Proyecto 1",
    //         description: "",
    //         source: ""
    //     },
    //     {
    //         title: "Proyecto 2",
    //         description: "",
    //         source: ""
    //     },
    //     {
    //         title: "Proyecto 3",
    //         description: "",
    //         source: ""
    //     },
    // ];

    if (!cardsContainer.hasChildNodes() && cards.length > 0)
        cards.map(card => {
            const cardElement = cardComponent(card["title"], card["description"], card["source"]["source"]);
            cardsContainer.appendChild(cardElement);
        });
}