var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
export const getInfo = (endpoint, token) => __awaiter(void 0, void 0, void 0, function* () {
    const res = yield fetch(`http://localhost:5000/api/${endpoint}`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
    return res;
});
export const uploadInfo = (endpoint, token, data) => __awaiter(void 0, void 0, void 0, function* () {
    const res = yield fetch(`http://localhost:5000/api/${endpoint}`, {
        headers: {
            Authorization: `Bearer ${token}`
        },
        method: "POST",
        body: data
    });
    return res;
});
export const modifyInfo = (endpoint, token, data, elementId) => __awaiter(void 0, void 0, void 0, function* () {
    const res = yield fetch(`http://localhost:5000/api/${endpoint}/${elementId}`, {
        headers: {
            "Authorization": `Bearer ${token}`,
        },
        method: "PATCH",
        body: data
    });
    return res;
});
export const auth = (data) => __awaiter(void 0, void 0, void 0, function* () {
    const res = yield fetch(`http://localhost:5000/api/auth`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });
    return res;
});
