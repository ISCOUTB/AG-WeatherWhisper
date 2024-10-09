from flask import Flask, render_template, request, jsonify, redirect, url_for
from weather_api import get_weather, get_coordinates, get_clothing_recommendation  # Importa las funciones necesarias

app = Flask(__name__)

# Ruta para servir el index.html
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para servir el login.html
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Aquí debes validar el usuario (ej. compararlo con una base de datos)
        if username == "usuario" and password == "contraseña":  # Ejemplo de validación
            return redirect(url_for('index'))  # Redirigir al index si el login es exitoso
        else:
            return "Credenciales incorrectas", 401  # Manejo de error

    return render_template('login.html')

# Ruta para servir el register.html
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Aquí debes guardar el usuario (ej. en una base de datos)
        # Simulando registro exitoso
        return redirect(url_for('index'))  # Redirigir al index después del registro
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
    app.run(debug=True)
