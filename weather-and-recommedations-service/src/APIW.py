from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY_TOMORROW = "ud4J9RTtncJIFktrHWfpN59y3VLVVfhb"
API_KEY_OPENCAGE = "097aba7edfda4d57b2810b642abd29f1"  # Reemplaza con tu clave de OpenCage

def get_coordinates(city_name):
    # URL de la API de OpenCage
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city_name}&key={API_KEY_OPENCAGE}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            # Retorna las coordenadas de la primera coincidencia
            coordinates = data['results'][0]['geometry']
            return (coordinates['lat'], coordinates['lng'])
        else:
            return None
    else:
        return None

def get_weather(location):
    # URL de la API de Tomorrow.io
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={location}&apikey={API_KEY_TOMORROW}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def get_clothing_recommendation(temperature, weather_code):
    if temperature < 0:
        return "Usa un abrigo pesado, guantes y una bufanda."
    elif 0 <= temperature < 15:
        return "Usa una chaqueta cálida, pantalones largos y un suéter."
    elif 15 <= temperature < 25:
        return "Una chaqueta ligera o suéter y pantalones largos son adecuados."
    else:
        if weather_code == 2100:  # Aquí puedes ajustar según los códigos que desees
            return "Vístete con una camiseta ligera y shorts."
        return "Vístete con una camiseta y pantalones cortos."

@app.route('/recommendation', methods=['GET'])
def recommendation():
    city_name = request.args.get('city')
    if not city_name:
        return jsonify({"error": "City parameter is required"}), 400

    location = get_coordinates(city_name)

    if location:
        weather_data = get_weather(f"{location[0]},{location[1]}")
        
        if weather_data:
            # Imprimir los datos del clima para verificar la estructura
            print("Datos del clima:", weather_data)

            try:
                # Acceder a los datos
                temperature = weather_data['data']['values']['temperature']
                weather_code = weather_data['data']['values']['weatherCode']
                
                recommendation = get_clothing_recommendation(temperature, weather_code)
                return jsonify({
                    "city": city_name,
                    "coordinates": location,
                    "temperature": temperature,
                    "weatherCode": weather_code,
                    "recommendation": recommendation
                })
            except KeyError as e:
                return jsonify({"error": f"Missing key in response: {str(e)}"}), 500

        return jsonify({"error": "Unable to retrieve weather data"}), 500

    return jsonify({"error": "Unable to retrieve coordinates"}), 500

if __name__ == '__main__':
    app.run(debug=True)
