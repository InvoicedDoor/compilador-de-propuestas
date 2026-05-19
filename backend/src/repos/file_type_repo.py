from src.utilities.logger.logger import Logger
from src.models.file_type_model import FileTypeModel, MimeTypeModel
from sqlalchemy.orm import joinedload, Session
from sqlalchemy import select
import traceback

def get_file_tipes_repo(session: Session):

    try:

        query = (
            select(FileTypeModel)
            .options(
                joinedload(FileTypeModel.mime)
            )
        )

        result = session.execute(query)

        file_tipes = result.scalars().all()

        return file_tipes

    except:

        Logger.add_to_log(
            'error',
            traceback.format_exc()
        )

        raise ValueError(
            "Error al obtener los tipos de archivos."
        )
