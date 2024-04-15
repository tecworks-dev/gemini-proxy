from flask import Flask, request, jsonify, Response
import requests

app = Flask(__name__)

API_URL = "https://generativelanguage.googleapis.com/"

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    """
    Transparent reverse proxy to forward requests to the Google Generative Language API.

    Args:
    path (str): The API path that is appended to the base URL.

    Returns:
    Response object: The response from the Google API, forwarded back to the client.
    """
    url = f"{API_URL}{path}"

    # Forward the headers
    headers = dict(request.headers)

    # Ensure we delete content-length if present because it may cause issues if the proxy modifies the request slightly.
    headers.pop('Content-Length', None)

    # Forward the method
    method = request.method

    # Handle different request methods
    if method == 'GET':
        resp = requests.get(url, headers=headers, params=request.args)
    elif method == 'POST':
        resp = requests.post(url, headers=headers, json=request.json, params=request.args)
    elif method == 'PUT':
        resp = requests.put(url, headers=headers, json=request.json, params=request.args)
    elif method == 'DELETE':
        resp = requests.delete(url, headers=headers, params=request.args)

    # Create a response object and mimic the upstream server's response
    response = Response(resp.content, resp.status_code)
    response.headers.extend(resp.headers)

    # Return the proxied response
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
