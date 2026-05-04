export const showToast = (message, type = "info") => {
    const styles = {
        success: "#4caf50",
        error: "#e53935",
        warning: "#f9a825",
        info: "#546e7a"
    };
    const borderColor = styles[type];
    Toastify({
        text: message,
        duration: 3000,
        gravity: "top",
        position: "right",
        stopOnFocus: true,
        style: {
            background: "#2b2b2b",
            color: "#e0e0e0",
            borderLeft: `4px solid ${borderColor}`,
            borderRadius: "6px",
            boxShadow: "none",
            fontSize: "0.9rem"
        }
    }).showToast();
};
