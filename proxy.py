from flask import Flask, request, jsonify, Response, after_this_request
import requests
import logging

app = Flask(__name__)

API_URL = "https://generativelanguage.googleapis.com/"

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    headers.pop('Content-Length', None)

    # Forward the method
    method = request.method

    # Log the incoming request
    logger.info(f"Request {method} to {url} with headers {headers} and query {request.args}")

    # Handle different request methods
    if method == 'GET':
        resp = requests.get(url, headers=headers, params=request.args)
    elif method == 'POST':
        resp = requests.post(url, headers=headers, json=request.json, params=request.args)
    elif method == 'PUT':
        resp = requests.put(url, headers=headers, json=request.json, params=request.args)
    elif method == 'DELETE':
        resp = requests.delete(url, headers=headers, params=request.args)

    @after_this_request
    def log_response(response):
        # Log the response
        logger.info(f"Response from {url} with status {resp.status_code} and headers {resp.headers}")
        return response

    # Create a response object and mimic the upstream server's response
    response = Response(resp.content, resp.status_code)
    response.headers.extend(resp.headers)

    # Return the proxied response
    return response

if __name__ == '__main__':
    
    logger.info(f"Ready to receive requests")
    app.run(debug=True, host='0.0.0.0', port=5000)
