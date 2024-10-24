import pyodbc
import bcrypt

# Conexión a la base de datos Microsoft SQL Server
def get_db_connection():
    try:
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=weatherwishperapp.database.windows.net;'
            'DATABASE=weatherwhisper;'
            'UID=rootw;'
            'PWD=Vialmar7;'
        )
        return connection
    except Exception as e:
        print("Error al conectarse a la base de datos:", e)
        return None

# Registro de usuario en la base de datos
def register_user(name, email, password, phone_number):
    conn = get_db_connection()
    if conn is None:
        return False  # Si no hay conexión, regresar False

    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password, phone_number) VALUES (?, ?, ?, ?)", 
            (name, email, hashed_password, phone_number)
        )
        conn.commit()
        return True  # Registro exitoso
    except Exception as e:
        print("Error al registrar el usuario:", e)
        return False
    finally:
        cursor.close()
        conn.close()

# Validación de usuario al iniciar sesión
def validate_user(name, password):
    conn = get_db_connection()
    if conn is None:
        return False  # Si no hay conexión, regresar False

    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE name = ?", (name,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[0]):
        return True
    return False
