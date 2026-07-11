const BACKEND_uRL = "http://localhost:5000";

export const getInfo = async (endpoint: string, token: string) => {
    const res = await fetch(`${BACKEND_uRL}/api/${endpoint}`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });

    return res
}

export const uploadInfo = async (endpoint: string, token: string, data: any) => {
    const res = await fetch(`${BACKEND_uRL}/api/${endpoint}`, {
        headers: {
            Authorization: `Bearer ${token}`
        },
        method: "POST",
        body: data
    });

    return res;
}

export const modifyInfo = async (endpoint: string, token: string, data: any, elementId: Number) => {
    const res = await fetch(`${BACKEND_uRL}/api/${endpoint}/${elementId}`, {
        headers: {
            "Authorization": `Bearer ${token}`,
        },
        method: "PATCH",
        body: data
    });

    return res
}

export const auth = async (data: any) => {
    const res = await fetch(`${BACKEND_uRL}/api/auth`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    return res;
}

export const register = async (endpoint: string, data: any) => {
    const res = await fetch(`${BACKEND_uRL}/api/${endpoint}`, {
        headers: {
            "Content-Type": "application/json"
        },
        method: "POST",
        body: JSON.stringify(data)
    });

    return res;
}
