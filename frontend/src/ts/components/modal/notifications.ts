declare function Toastify(options: {
    text: string;
    duration?: number;
    gravity?: "top" | "bottom";
    position?: "left" | "center" | "right";
    stopOnFocus?: boolean;
    style?: Record<string, string>;
}): {
    showToast(): void;
};

type ToastType = "success" | "error" | "warning" | "info";

export const showToast = (
    message: string,
    type: ToastType = "info"
): void => {

    const styles: Record<ToastType, string> = {
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