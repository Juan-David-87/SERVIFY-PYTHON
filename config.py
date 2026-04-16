import os

class Config:
    # 🔐 Clave secreta para sesiones
    SECRET_KEY = os.getenv("SECRET_KEY", "clave_super_secreta")

    # 🗄️ Configuración de la base de datos
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "servifyprueba")