import os

from datetime import datetime
from secrets import token_urlsafe

import requests
from flask import Flask, jsonify


app = Flask(__name__)

counter = 0

@app.get('/webhook/')
def index():
    global counter
    
    payload = {
        "id": token_urlsafe(16),
        "timestamp": datetime.now().isoformat(),
        "event": "webhook",
        "data": {
            "counter": counter
        }
    }
    
    response = requests.post(
        url="https://private.nbdev.com.br",
        json=payload,
        verify=os.path.join(os.path.dirname(__file__), "ca.crt"),
        cert=(
            os.path.join(os.path.dirname(__file__), "client.crt"),
            os.path.join(os.path.dirname(__file__), "client.key"),
        ),
    )
    
    counter += 1
    
    return jsonify({
        "status": "success" if response.status_code == 200 else "failure",
        "response": response.json() if response.status_code == 200 else response.text,
        "payload": payload,
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
