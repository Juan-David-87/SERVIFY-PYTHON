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
def create_user(name, email, phone, password_hash, role):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO users (name, email, phone, password_hash, role)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (name, email, phone, password_hash, role))

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

def get_all_services():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()

    cursor.close()
    conn.close()

    return services

def create_worker_service(user_id, service_id, price):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO worker_services (worker_id, service_id, price)
        VALUES (%s, %s, %s)
    """

    cursor.execute(sql, (user_id, service_id, price))

    conn.commit()
    cursor.close()
    conn.close()

def get_services_by_worker(worker_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT s.name, ws.price
        FROM worker_services ws
        JOIN services s ON ws.service_id = s.id
        WHERE ws.worker_id = %s
    """

    cursor.execute(sql, (worker_id,))
    servicios = cursor.fetchall()

    cursor.close()
    conn.close()

    return servicios