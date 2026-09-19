import BaseStorage from "../class/BaseStrage.js";
import { showToast } from "../components/modal/notifications.js";
import { getInfo } from "../functions/apiConnection.js";

interface ProjectRoleState {
    code: string
    description: string
}

interface ProjectRoleStorageState {
    roles: ProjectRoleState[]
}

class ProjectRoleStorage extends BaseStorage<ProjectRoleStorageState> {
    constructor() {
        super("project_info_store", {
            roles: []
        })

        this.store.roles = []
    }

    public projectRolesActions = {
        loadInfo: async (): Promise<void> => {
            const token = localStorage.getItem("token")

            if (!token)
            {
                location.href = "/";
                return;
            }

            const res = await getInfo("project-roles", token)

            const jsonResult = await res.json();

            if (!res.ok)
            {
                showToast(jsonResult.message, "warning");
                return;
            }

            if (this.store.roles.length === 0)
                this.store.roles = jsonResult.data;
        }
    }
}

const projectRolesStore = new ProjectRoleStorage()

export default projectRolesStore;