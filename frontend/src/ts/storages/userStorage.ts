import BaseStorage from "../class/BaseStrage.js";

interface UserState {
    name: string;
    role: string;
}

class UserStorage extends BaseStorage<UserState> {
    constructor() {
        super("user_store", {
            name: "",
            role: ""
        });
    }

    public userActions = {
        login: (username: string, role: UserState['role']) => {
            this.store.name = username;
            this.store.role = role;
        },
        logout: () => {
            localStorage.clear();
            location.href = "/login";
        }
    };

}

const userStore = new UserStorage()

export default userStore;