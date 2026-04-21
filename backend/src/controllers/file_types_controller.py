
from src.utilities.middlewares.veryfy_authentication import verify_authentication
from ..services.filte_type_service import get_file_types_service
from flask import Blueprint, jsonify
from src.utilities.logger.logger import Logger
import traceback

main = Blueprint('file_types_blueprint', __name__)

@main.get('')
@verify_authentication
def get_all_proposals_route():
    try:
        file_types = get_file_types_service()

        return jsonify({
            "data": file_types,
            "message": "Datos encontrados."
        })
    except Exception as ex:
        Logger.add_to_log('error', traceback.format_exc())
        return 'Error', 500
