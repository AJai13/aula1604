# recommendation_api_a.py
from flask import Flask, jsonify
import requests
import redis
import json

app = Flask(__name__)

API_B_URL = "http://localhost:5001/weather/"
CACHE_DURATION = 60

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@app.route('/recommendation/<city>', methods=['GET'])
def get_recommendation(city):
    cache_key = f"weather:{city}"

    cached_data = r.get(cache_key)
    if cached_data:
        print(f"Cache HIT para {city}")
        return jsonify(json.loads(cached_data))
        
    try:
        response = requests.get(API_B_URL + city)
        if response.status_code == 404:
            return jsonify({"error": "Cidade não encontrada na API B"}), 404

        response.raise_for_status()
        data = response.json()
        temp = data["temp"]

        if temp > 30:
            recommendation = "Está muito quente! Hidrate-se e use protetor solar."
        elif temp > 15:
            recommendation = "O clima está agradável, aproveite o dia!"
        else:
            recommendation = "Está frio! Não esqueça seu casaco."


        result = {
            "city": data["city"],
            "temp": data["temp"],
            "unit": data["unit"],
            "recommendation": recommendation
        }

        r.setex(cache_key, CACHE_DURATION, json.dumps(result))
        print(f"Cache SET para {city}")
        
        return jsonify(result)

    except requests.exceptions.RequestException:
        return jsonify({"error": "Erro ao conectar com a API B"}), 500
    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=5000)
