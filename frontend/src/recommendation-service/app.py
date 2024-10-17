from flask import Flask, request, jsonify
from weather_api import get_weather, get_coordinates
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Ruta para obtener recomendaciones de vestimenta basado en la temperatura
@app.route('/recommendation', methods=['GET'])
def recommendation():
    city_name = request.args.get('city')
    if not city_name:
        return jsonify({"error": "El parámetro 'city' es obligatorio."}), 400
    
    # Obtener coordenadas de la ciudad
    location = get_coordinates(city_name)
    if location:
        weather_data = get_weather(f"{location[0]},{location[1]}")
        if weather_data:
            try:
                temperature = weather_data['data']['values']['temperature']
                recommendation = get_clothing_recommendation(temperature)
                return jsonify({
                    "city": city_name,
                    "coordinates": location,
                    "temperature": temperature,
                    "recommendation": recommendation,
                })
            except KeyError as e:
                return jsonify({"error": f"Falta la clave: {str(e)}"}), 500
        return jsonify({"error": "No se pudo obtener los datos del clima"}), 500
    return jsonify({"error": "No se pudieron obtener las coordenadas"}), 500

def get_clothing_recommendation(temperature):
    if temperature < 0:
        return "Usa un abrigo pesado, guantes y una bufanda."
    elif 0 <= temperature < 15:
        return "Usa una chaqueta cálida, pantalones largos y un suéter."
    elif 15 <= temperature < 25:
        return "Una chaqueta ligera o suéter y pantalones largos son adecuados."
    else:
        return "Vístete con una camiseta ligera y shorts."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002)
