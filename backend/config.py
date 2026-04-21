from dotenv import load_dotenv
import os

load_dotenv()

class Config():
    SECRET_KEY = os.getenv('SECRET_KEY')
    
class DevelopmentConfig(Config):
    DEBUG=True

class ProductionConfig(Config):
    DEBUG=False

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}

routes = ['GET','POST','PUT','DELETE','PATCH','OPTIONS','HEAD']
