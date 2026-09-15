import BaseStorage from "../class/BaseStrage.js";

export interface ProjectInfoState {
    id: number;
    title: string;
    description: string;
    project_events: Array<ProjectEventInterface>;
    active: boolean;
    files: Array<FilesInterface>;
}

interface ProjectEventInterface {
    name: string;
    first_lastname: string;
    second_lastname: string;
    role: CompanyRoleInterface;
    approved: boolean;
}

interface CompanyRoleInterface {
    code: string;
    role: string;
}

interface FilesInterface {
    id: number;
    filename: string;
    path: string;
}

class ProjectInfoStorage extends BaseStorage<ProjectInfoState> {
    constructor() {
        super("project_info_store", {
            id: 0,
            title: "",
            description: "",
            files: [],
            project_events: [],
            active: false
        })
    }

    public projectInfoActions = {
        setInfo: (projectInfo: ProjectInfoState) => {
            this.store.id = projectInfo.id;
            this.store.title = projectInfo.title;
            this.store.description = projectInfo.description;
            this.store.project_events = projectInfo.project_events;
            this.store.active = projectInfo.active;
            this.store.files = projectInfo.files;
        }
    }
}

const projectInfoStore = new ProjectInfoStorage()

export default projectInfoStore;