import psycopg2
import bcrypt

# Conexión a la base de datos PostgreSQL
def get_db_connection():
    connection = psycopg2.connect(
        host="localhost", 
        database="weatherwhisper",
        user="postgres",
        password="Golgol123/"
    )
    return connection 

# Registro de usuario en la base de datos
def register_user(name, email, password, phone_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password, phone_number) VALUES (%s, %s, %s, %s)", 
            (name, email, hashed_password, phone_number)
        )
        conn.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()

# Validación de usuario al iniciar sesión
def validate_user(name, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE name = %s", (name,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
        return True
    return False
