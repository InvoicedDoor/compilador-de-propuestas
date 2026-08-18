type FileType = string | "Portada";

export interface FileInterface {
    id: number,
    filename: string,
    path: string
}

export interface Metadata {
    id: number;
    type: FileType;
    name: string;
}

export interface Preview {
    id: number;
    url: string;
}