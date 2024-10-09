from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

API_KEY_TOMORROW = "gcRChK23DGmoCYen6tVm3XX73Jxfuwh9"
API_KEY_OPENCAGE = "8795cc1289d9432297a2a878903f3891"

# Ruta para servir el index.html
@app.route('/')
def index():
    return render_template('index.html')

def get_coordinates(city_name):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city_name}&key={API_KEY_OPENCAGE}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            coordinates = data['results'][0]['geometry']
            return (coordinates['lat'], coordinates['lng'])
    return None

def get_weather(location):
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={location}&apikey={API_KEY_TOMORROW}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    return None

def get_clothing_recommendation(temperature):
    if temperature < 0:
        return "Usa un abrigo pesado, guantes y una bufanda."
    elif 0 <= temperature < 15:
        return "Usa una chaqueta cálida, pantalones largos y un suéter."
    elif 15 <= temperature < 25:
        return "Una chaqueta ligera o suéter y pantalones largos son adecuados."
    else:
        return "Vístete con una camiseta ligera y shorts."

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
                    "temperature": temperature,
                    "recommendation": recommendation
                })
            except KeyError as e:
                return jsonify({"error": f"Falta la clave: {str(e)}"}), 500
        return jsonify({"error": "No se pudo obtener los datos del clima"}), 500
    return jsonify({"error": "No se pudieron obtener las coordenadas"}), 500

if __name__ == '__main__':
    app.run(debug=True)
