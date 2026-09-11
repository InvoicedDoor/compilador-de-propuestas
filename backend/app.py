from src import init_app
from config import config
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

def create_new_path(log_directory: str, log_file: str):
    log_path_directory = Path(log_directory)

    if not log_path_directory.exists():
        log_path_directory.mkdir(parents=True, exist_ok=True)

    log_path_file = log_path_directory / log_file

    if not log_path_file.exists():
        log_path_file.touch()

system_log_directory = os.getenv("DEFAULT_LOGGER_DIRECTORY")
system_log_file = os.getenv("DEFAULT_LOGGER_FILENAME")

events_logger_directory = os.getenv("EVENTS_LOGGER_DIRECTORY")
events_logger_filename = os.getenv("EVENTS_LOGGER_FILENAME")

test_logger_directory = os.getenv("TEST_LOGGER_DIRECTORY")
test_logger_filename = os.getenv("TEST_LOGGER_FILENAME")

try:
    if (not system_log_file
        or not system_log_directory
        or not events_logger_directory
        or not events_logger_filename
        or not test_logger_directory
        or not test_logger_filename):
        raise Exception("Faltan argumentos en las variables de entorno.")
    configuration = config['development']

    create_new_path(system_log_directory, system_log_file)
    create_new_path(events_logger_directory, events_logger_filename)
    create_new_path(test_logger_directory, test_logger_filename)

    app = init_app(configuration)
    if __name__ == '__main__':
        app.run(debug=False,
                host="0.0.0.0",
                port=5000)
        
except Exception as ex:
    print(ex)
    print("Error al iniciar el servidor.")