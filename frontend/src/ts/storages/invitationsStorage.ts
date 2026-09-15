import BaseStorage from "../class/BaseStrage.js";

export interface InvitationState {
    id: number
    mail: string
}

class InvitationStorage extends BaseStorage<Array<InvitationState>> {
    private invitationCounter: number;
    constructor() {
        super("invitations_store", []);
        this.invitationCounter = this.store.reduce(
            (max, invitation) =>
                Math.max(max, invitation.id),
            0
        );
    }

    public invitationActions = {
        addRecipient: (recipient: InvitationState): void => {
                const id = ++ this.invitationCounter;
                recipient.id = id;
                this.store.push(recipient);
        }
    };

}

const invitationStore = new InvitationStorage()

export default invitationStore;