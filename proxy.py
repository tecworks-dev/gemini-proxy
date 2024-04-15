from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_URL = "https://generativelanguage.googleapis.com/"

@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    """
    Proxy to forward requests to the Google Generative Language API.

    Args:
    path (str): The API path that is appended to the base URL.

    Returns:
    Response object: The response from the Google API, forwarded back to the client.
    """
    url = f"{API_URL}{path}"
    if request.method == 'GET':
        resp = requests.get(url, params=request.args)
    elif request.method == 'POST':
        resp = requests.post(url, json=request.json, params=request.args)

    return jsonify(resp.json()), resp.status_code

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
