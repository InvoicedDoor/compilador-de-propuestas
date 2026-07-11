from src.utilities.logger.logger import Logger
from src.models.file_type_model import FileTypeModel, MimeTypeModel, MimeTypeExtensionTable, MimeCategoryModel
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
import traceback

def get_file_tipes_repo(session: Session):

    try:

        query = (
            select(FileTypeModel)
            .options(
                selectinload(FileTypeModel.mime_type_extension)
                .selectinload(MimeTypeExtensionTable.extension),
                
                selectinload(FileTypeModel.mime_type_extension)
                .selectinload(MimeTypeExtensionTable.mime_type)
            )
        )

        result = session.execute(query)

        return result.unique().scalars().all()

    except:

        Logger.add_to_log(
            'error',
            traceback.format_exc()
        )

        raise ValueError(
            "Error al obtener los tipos de archivos."
        )
