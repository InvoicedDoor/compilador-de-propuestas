from flask import Flask, jsonify
from marshmallow import ValidationError
from flask_cors import CORS
from src.controllers import (
    user_controller,
    auth_controller, 
    project_controller, 
    register_controller,
    file_types_controller, 
    )
from src.controllers.project_roles.controller import main_project_roles
from src.utilities.handlers.http_exceptions import DomainError
from src.websocket.controller import sock

app = Flask(__name__)

# sock.init_app(app)

app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB

CORS(app)

@app.errorhandler(DomainError)
def handle_domain_error(error):
    
    return jsonify(
        error.to_dict()
    ), error.status_code

@app.errorhandler(ValidationError)
def handle_domain_error(error):
    
    return jsonify({
        "message": "Error de validación.",
        "errors": error.messages
    }), 422

def init_app(config):
    try:
        app.config.from_object(config)
        app.register_blueprint(auth_controller.main, url_prefix='/api/auth')
        app.register_blueprint(register_controller.main, url_prefix='/api/register')
        app.register_blueprint(user_controller.main, url_prefix='/api/users')
        app.register_blueprint(project_controller.main, url_prefix='/api/project')
        app.register_blueprint(file_types_controller.main, url_prefix='/api/file-tipes')
        app.register_blueprint(main_project_roles, url_prefix='/api/project-roles')

        return app
    except Exception as ex:
        raise