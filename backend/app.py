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
    if not Path.exists(f"{log_directory}/{log_file}"):
        Path.mkdir(f"{log_directory}/{log_file}")
    app = init_app(configuration)
    if __name__ == '__main__':
        app.run(debug=False,
                host="0.0.0.0",
                port=5000)
        
except Exception as ex:
    print("Error al iniciar el servidor.")