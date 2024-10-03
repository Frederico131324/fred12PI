from flask import Flask, jsonify, send_from_directory
import requests
import hmac
import hashlib
import time
import os

app = Flask(__name__)

API_KEY = 'uNvM5iwyu6zZ0CDCyAYau0BSJNz10R5MYkAVZ2dmxRIqFXrAozrLW8mI5C6rEHSM'
API_SECRET = 'uNBGeehuLlKct889rUpCGocLRlqWLjwDW95Ju4sCAvswyOBjhdDiYV5ILc2pJQAq'
BASE_URL = 'https://api.binance.com'

def create_signature(query_string):
    return hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()

@app.route('/')
def serve_index():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route('/api/account')
def get_account_info():
    timestamp = int(time.time() * 1000)
    query_string = f'timestamp={timestamp}'
    signature = create_signature(query_string)

    url = f"{BASE_URL}/api/v3/account?{query_string}&signature={signature}"

    headers = {
        'X-MBX-APIKEY': API_KEY
    }

    response = requests.get(url, headers=headers)

    if response.ok:
        return jsonify(response.json())
    else:
        return jsonify({'error': response.text}), response.status_code

@app.route('/api/deposit-history')
def get_deposit_history():
    timestamp = int(time.time() * 1000)
    query_string = f'timestamp={timestamp}'
    signature = create_signature(query_string)

    url = f"{BASE_URL}/sapi/v1/capital/deposit/hisrec?{query_string}&signature={signature}"

    headers = {
        'X-MBX-APIKEY': API_KEY
    }

    response = requests.get(url, headers=headers)

    # Log da resposta
    print("Resposta da API de depósitos:", response.text)  # Adicione este log

    if response.ok:
        return jsonify(response.json())
    else:
        return jsonify({'error': response.text}), response.status_code


@app.route('/api/withdrawal-history')
def get_withdrawal_history():
    timestamp = int(time.time() * 1000)
    query_string = f'timestamp={timestamp}'
    signature = create_signature(query_string)

    url = f"{BASE_URL}/sapi/v1/capital/withdraw/history?{query_string}&signature={signature}"

    headers = {
        'X-MBX-APIKEY': API_KEY
    }

    response = requests.get(url, headers=headers)

    if response.ok:
        return jsonify(response.json())
    else:
        return jsonify({'error': response.text}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
