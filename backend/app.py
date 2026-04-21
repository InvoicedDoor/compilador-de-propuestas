from src import init_app
from config import config

try:
    configuration = config['development']
    app = init_app(configuration)
    if __name__ == '__main__':
        app.run(debug=True,
                port=5000)
        
except Exception as ex:
    print("Error al iniciar el servidor.")