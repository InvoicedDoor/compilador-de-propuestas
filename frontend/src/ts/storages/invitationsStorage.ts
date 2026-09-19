import BaseStorage from "../class/BaseStrage.js";

export interface InvitationInterface {
    mail: string;
    project_role: string;
}

interface InvitationState {
    users: InvitationInterface[];
}

class InvitationStorage extends BaseStorage<InvitationState> {
    constructor() {
        super("invitations_store", {
            users: []
        });
        this.store.users = []
    }

    public invitationActions = {
        addUser: (user: InvitationInterface): void => {
            this.store.users.push(user);
        },
        deleteUser: (mail: string): void => {
            this.store.users = this.store.users.filter(user => user.mail !== mail)
        },
        destroy: (): void => {
            this.store.users = []
        }
    };

}

const invitationStore = new InvitationStorage()

export default invitationStore;