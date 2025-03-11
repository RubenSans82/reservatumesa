# config.py
import os

class Config:
    # Clave secreta para la sesión de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', '123456')

    # Datos de conexión a la base de datos
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_NAME = os.environ.get('DB_NAME', 'reservatumesa')

    # Otras configuraciones que requieras...