from dotenv import load_dotenv
import os, json

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

json_config = {}

with open("./src/utilities/json_configurations/project_status.json", "r", encoding="utf-8") as archivo:
    json_config = json.load(archivo)


APPROVAL_STEPS = json_config["steps"]

ROLE_APPROVER_PROJECT = json_config["role_approver_project"]

ALTERNATIVE_STATUS = []

CLOSER_STATUS = []

BACKEND_URL = os.getenv("BACKEND_URL")

CAN_MODIFY_PROJECT_PROPERTIES = json_config["can_modify_project_properties"]

for status in range(len(json_config["alternative_status"])):
    ALTERNATIVE_STATUS.append(json_config["alternative_status"][f"STATE_{status+1}"]["status"])

for status in range(len(json_config["closed_status"])):
    CLOSER_STATUS.append(json_config["closed_status"][f"STATE_{status+1}"]["status"])

routes = ['GET','POST','PUT','DELETE','PATCH','OPTIONS','HEAD']
