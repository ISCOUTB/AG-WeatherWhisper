from flask import Flask, render_template, request, jsonify, redirect, url_for
from weather_api import get_weather, get_coordinates, get_clothing_recommendation  # Importa las funciones necesarias
import psycopg2
import bcrypt


app = Flask(__name__)

def test_db_connection():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT 1')  # Una consulta simple para verificar la conexión
        cursor.close()
        conn.close()
        print("Conexión a la base de datos exitosa")
    except Exception as e:
        print("Error de conexión a la base de datos:", e)



# Configura la conexión a tu base de datos PostgreSQL
def get_db_connection():
    connection = psycopg2.connect(
        host="localhost",  # Cambia esto si tu base de datos está en otro lugar
        database="weatherwhisper",
        user="postgres",
        password="Golgol123/"
    )
    return connection

def register_user(name, email, password, phone_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO users (name, email, password, phone_number) VALUES (%s, %s, %s, %s)", (name, email, hashed_password, phone_number))
        conn.commit()
    except Exception as e:
                print("Error al registrar el usuario:", e)  # Imprime cualquier error
    cursor.close()
    conn.close()

def validate_user(name, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE name = %s", (name,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8'))
    return False



# Ruta para servir el index.html
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        
        if validate_user(name, password):
            return redirect(url_for('index'))  # Redirigir al index si el login es exitoso
        else:
            error_message = "Credenciales incorrectas. Intenta nuevamente."
            return render_template('login.html', error=error_message)  # Mostrar mensaje de error

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        phone_number = request.form.get('phone_number')

        # Validación básica para evitar que los campos estén vacíos
        if not name or not email or not password or not phone_number:
            error_message = "Todos los campos son obligatorios."
            return render_template('register.html', error=error_message)
        
        try:
            register_user(name, email, password, phone_number)  # Guardar el nuevo usuario en la base de datos
            print("Registro completado, redirigiendo al login...")
            return redirect(url_for('login'))  # Redirigir al login después del registro
        except Exception as e:
            print("Error al registrar el usuario:", e)
            return "Error al registrar el usuario", 500  # Enviar mensaje de error si falla

    return render_template('register.html')




# Ruta para obtener los datos del clima y recomendaciones
@app.route('/recommendation', methods=['GET'])
def recommendation():
    city_name = request.args.get('city')
    if not city_name:
        return jsonify({"error": "El parámetro 'city' es obligatorio."}), 400
    
    location = get_coordinates(city_name)
    if location:
        weather_data = get_weather(f"{location[0]},{location[1]}")
        if weather_data:
            try:
                temperature = weather_data['data']['values']['temperature']
                recommendation = get_clothing_recommendation(temperature)
                return jsonify({
                    "city": city_name,
                    "cordinates": location,
                    "temperature": temperature,
                    "recommendation": recommendation,
                })
            except KeyError as e:
                return jsonify({"error": f"Falta la clave: {str(e)}"}), 500
        return jsonify({"error": "No se pudo obtener los datos del clima"}), 500
    return jsonify({"error": "No se pudieron obtener las coordenadas"}), 500



if __name__ == '__main__':
    test_db_connection()  # Verifica la conexión al inicio
    app.run(host="0.0.0.0", port=5000,debug=True)

