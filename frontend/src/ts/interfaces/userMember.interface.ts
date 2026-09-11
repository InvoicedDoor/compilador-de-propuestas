import { CompanyRolInterface, ProjectRolInterface } from "../interfaces/rol.interface";

export interface UserMemberInterface {
    id: number
    name: string
    rol: ProjectRolInterface,
    position: CompanyRolInterface
}