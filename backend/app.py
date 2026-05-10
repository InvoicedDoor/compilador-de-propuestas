from src import init_app
from config import config
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

log_directory = os.getenv("DEFAULT_LOGGER_DIRECTORY")
log_file = os.getenv("DEFAULT_LOGGER_FILENAME")

try:
    configuration = config['development']
    
    log_path_directory = Path(log_directory)

    if not log_path_directory.exists():
        log_path_directory.mkdir(parents=True, exist_ok=True)

    log_path_file = log_path_directory / log_file

    if not log_path_file.exists():
        log_path_file.touch()

    app = init_app(configuration)
    if __name__ == '__main__':
        app.run(debug=False,
                host="0.0.0.0",
                port=5000)
        
except Exception as ex:
    print(ex)
    print("Error al iniciar el servidor.")