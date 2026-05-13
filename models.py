import pymysql
import pymysql.cursors
from config import Config

def get_connection():
    return pymysql.connect(
        host='127.0.0.1',
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )

def create_user(name, email, phone, password_hash, role):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO users (name, email, phone, password_hash, role) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (name, email, phone, password_hash, role))
    conn.commit()
    cursor.close()
    conn.close()

def get_user_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT * FROM users WHERE email = %s"
    cursor.execute(sql, (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT id, name, email, phone, role FROM users WHERE id = %s"
    cursor.execute(sql, (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

def get_all_services():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()
    cursor.close()
    conn.close()
    return services

def create_worker_service(user_id, service_id, price):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO worker_services (worker_id, service_id, price) VALUES (%s, %s, %s)"
    cursor.execute(sql, (user_id, service_id, price))
    conn.commit()
    cursor.close()
    conn.close()

def get_services_by_worker(worker_id):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
    SELECT ws.id, s.name, ws.price 
    FROM worker_services ws 
    JOIN services s ON ws.service_id = s.id 
    WHERE ws.worker_id = %s
    """
    cursor.execute(sql, (worker_id,))
    servicios = cursor.fetchall()
    cursor.close()
    conn.close()
    return servicios

def delete_worker_service(service_id, worker_id):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM worker_services WHERE id = %s AND worker_id = %s"
    cursor.execute(sql, (service_id, worker_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_worker_services():
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
    SELECT 
        ws.id,
        u.name      AS nombre,
        s.name      AS tipo,
        ws.price    AS precio,
        u.phone     AS telefono
    FROM worker_services ws
    JOIN users    u ON ws.worker_id  = u.id
    JOIN services s ON ws.service_id = s.id
    """
    cursor.execute(sql)
    servicios = cursor.fetchall()
    cursor.close()
    conn.close()
    return servicios