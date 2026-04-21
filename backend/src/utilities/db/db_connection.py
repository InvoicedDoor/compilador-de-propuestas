from dotenv import load_dotenv
import os, pymysql

load_dotenv()

def connect_to_database():
    try:
        connection = pymysql.connect(
            host=os.getenv('HOST'),
            user=os.getenv('USER'),
            password=os.getenv('PASSWORD'),
            database=os.getenv('DATABASE'))
        if connection:
            return connection
        
        return pymysql.err.DatabaseError
    except Exception as ex:
        raise ValueError("No se pudo establecer conexión con la base de datos")