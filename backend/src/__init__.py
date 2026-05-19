from flask import Flask, jsonify
from flask_cors import CORS
from src.controllers import auth_controller, proposal_controller, file_types_controller
from src.utilities.handlers.http_exceptions import DomainError

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB

CORS(app)

@app.errorhandler(DomainError)
def handle_domain_error(error):
    
    return jsonify(
        error.to_dict()
    ), error.status_code

def init_app(config):
    try:
        app.config.from_object(config)
        app.register_blueprint(auth_controller.main, url_prefix='/api/auth')
        app.register_blueprint(proposal_controller.main, url_prefix='/api/proposal')
        app.register_blueprint(file_types_controller.main, url_prefix='/api/file-tipes')

        return app
    except Exception as ex:
        raise