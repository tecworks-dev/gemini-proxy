from flask import Flask, request, Response
import requests
import logging
import sys

# Setup logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
API_URL = "https://generativelanguage.googleapis.com/"

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    """
    A transparent reverse proxy to forward requests to an API.
    """
    url = f"{API_URL}{path}"
    headers = {key: value for key, value in request.headers if key != 'Host'}
    headers.pop('Content-Length', None)

    # Log the request
    logger.info(f"Forwarding request to {url} with method {request.method}")

    resp = requests.request(method=request.method, url=url, headers=headers, data=request.get_data(), params=request.args, allow_redirects=False)

    # Log the response
    logger.info(f"Received {resp.status_code} response from the upstream server")

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]

    # Correctly set headers for the response
    response = Response(resp.content, resp.status_code)
    for header in headers:
        response.headers[header[0]] = header[1]

    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
