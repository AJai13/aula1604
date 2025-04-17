# climate_api_b.py
from flask import Flask, jsonify

app = Flask(__name__)

# Mock de dados climáticos
mock_weather_data = {
    "SãoPaulo": 25,
    "RioDeJaneiro": 34,
    "Curitiba": 14,
    "Salvador": 32,
    "PortoAlegre": 16
}

@app.route('/weather/<city>', methods=['GET'])
def get_weather(city):
    temperature = mock_weather_data.get(city)
    if temperature is None:
        return jsonify({"error": "Cidade não encontrada"}), 404

    return jsonify({
        "city": city,
        "temp": temperature,
        "unit": "Celsius"
    })

if __name__ == '__main__':
    app.run(port=5001)
