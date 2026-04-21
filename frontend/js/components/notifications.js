export const showToast = (message, type = "info") => {
    let background = "#2b2b2b";
    let border = "4px solid #4caf50"; // success por default

    switch (type) {
        case "error":
            border = "4px solid #e53935";
            break;
        case "warning":
            border = "4px solid #f9a825";
            break;
        case "info":
            border = "4px solid #546e7a";
            break;
    }

    Toastify({
        text: message,
        duration: 3000,
        gravity: "top",
        position: "right",
        stopOnFocus: true,
        style: {
            background: background,
            color: "#e0e0e0",
            borderLeft: border,
            borderRadius: "6px",
            boxShadow: "none",
            fontSize: "0.9rem"
        }
    }).showToast();
};