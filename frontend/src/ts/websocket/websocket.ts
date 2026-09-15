export const socket = new WebSocket("ws://127.0.0.1:5000/ws");

socket.addEventListener("open", () => {
    console.log("WebSocket conectado");
});

socket.addEventListener("message", (event) => {
    console.log("Mensaje del servidor:", event.data);
});

socket.addEventListener("close", () => {
    console.log("WebSocket cerrado");
});

socket.addEventListener("error", (error) => {
    console.error("WebSocket error:", error);
});

declare global {
    interface Window {
        socket: WebSocket;
    }
}

window.socket = socket;
