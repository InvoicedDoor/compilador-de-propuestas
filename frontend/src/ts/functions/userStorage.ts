// 1. Definimos las interfaces para el Estado y las Acciones
export interface UserState {
    name: string;
    role: string; // Tipado literal estricto
}

// Interfaz para las funciones que escuchan los cambios
type StoreListener = (state: UserState) => void;

// 2. Funciones de Persistencia con manejo seguro de tipos
const loadFromStorage = (): UserState => {
    const data = localStorage.getItem('user_store');
    return data ? JSON.parse(data) : { name: "", role: "" };
};

const saveToStorage = (state: UserState): void => {
    localStorage.setItem('user_store', JSON.stringify(state));
};

// 3. Set de suscriptores tipado
const listeners = new Set<StoreListener>();

// Estado inicial con su tipo correspondiente
const baseState: UserState = loadFromStorage();

// 4. El Proxy con tipado estricto
export const userStore = new Proxy<UserState>(baseState, {
    set(target, property: keyof UserState, value) {
        // Aseguramos que la propiedad pertenezca a UserState
        (target[property] as typeof value) = value; // 1. Modifica en memoria
        saveToStorage(target);                       // 2. Guarda en disco
        listeners.forEach(fn => fn(target));         // 3. Notifica cambios
        return true;
    }
});

// 5. Función de suscripción tipada
export const subscribe = (callback: StoreListener): void => {
    listeners.add(callback);
    callback(userStore); // Render inicial
};

// 6. Acciones (Actions) con parámetros tipados
export const userActions = {
    login(username: string, role: UserState['role']): void {
        userStore.name = username;
        userStore.role = role;
    },
    logout(): void {
        userStore.name = "";
        userStore.role = "invitado";
    }
};
