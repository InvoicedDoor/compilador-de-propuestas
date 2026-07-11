export interface MimeModel {
    id: number,
    mime_pattern: string
    category: string
    extension: string
    icon: string
}

export default interface FileTypeModel {
    id: number;
    description: string
    mime: MimeModel
    is_main_image: boolean
    active: boolean
}