from src.utilities.logger.logger import Logger
from src.models.file_tipes.model import FileTypeModel
from src.models.mime_tipes.model import MimeTypeModel
from src.dtos.mime_tipes.dto import MimeTypeDto 
from sqlalchemy.orm import Session
from sqlalchemy import select
import traceback

def get_file_tipes_repo(session: Session):

    try:

        query = (
            select(FileTypeModel)
            .join(FileTypeModel.mime_type, isouter=True)
        )

        result = session.execute(query)

        return result.unique().scalars().all()

    except:

        Logger.add_to_system_log(
            'error',
            traceback.format_exc()
        )

        raise ValueError(
            "Error al obtener los tipos de archivos."
        )


def get_file_type_by_filter(session: Session, file_type: MimeTypeDto):
    try:
        query = select(MimeTypeModel)

        for field, value in file_type.model_dump(exclude_none=True).items():
            query = query.where(getattr(MimeTypeModel, field) == value)

        result = session.execute(query)

        return result.scalar_one_or_none()

    except:

        Logger.add_to_system_log(
            'error',
            traceback.format_exc()
        )

        raise ValueError(
            "Error al obtener los tipos de archivos."
        )
