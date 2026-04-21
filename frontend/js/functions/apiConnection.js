export const getInfo = async (endpoint, token) => {
    const res = await fetch(`http://localhost:5000/api/${endpoint}`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });

    return res
}

export const uploadInfo = async (endpoint, token, data) => {
    const res = await fetch(`http://localhost:5000/api/${endpoint}`, {
        headers: {
            Authorization: `Bearer ${token}`
        },
        method: "POST",
        body: data
    });

    return res;
}

export const modifyInfo = async (endpoint, token, data, elementId) => {
    const res = await fetch(`http://localhost:5000/api/${endpoint}/${elementId}`, {
        headers: {
            "Authorization": `Bearer ${token}`,
        },
        method: "PATCH",
        body: data
    });

    return res
}

export const auth = async (data) => {
    const res = await fetch(`http://localhost:5000/api/auth`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    return res;
}