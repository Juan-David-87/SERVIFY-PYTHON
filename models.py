import mysql.connector
from config import Config

# 🔌 Conexión a la base de datos
def get_connection():
    return mysql.connector.connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME
    )

# 📝 Crear usuario (registro)
def create_user(name, email, password_hash, role):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO users (name, email, password_hash, role)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (name, email, password_hash, role))

    conn.commit()
    cursor.close()
    conn.close()

# 🔍 Buscar usuario por email (login)
def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = "SELECT * FROM users WHERE email = %s"
    cursor.execute(sql, (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user

# 🔍 Buscar usuario por ID (para perfil después)
def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = "SELECT id, name, email, role FROM users WHERE id = %s"
    cursor.execute(sql, (user_id,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user