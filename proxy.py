from flask import Flask, request, Response
import requests
import logging
import sys

# Setup logging

def setup_logging():
    # Create a custom logger
    logger = logging.getLogger(__name__)
    
    # Set the log level
    logger.setLevel(logging.DEBUG)  # Can be INFO, DEBUG, WARNING, ERROR, CRITICAL

    # Create handlers
    c_handler = logging.StreamHandler(sys.stdout)  # Console handler
    f_handler = logging.FileHandler('processing.log')  # File handler
    
    # Create formatters and add them to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)
    
    # Set level for handlers
    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.DEBUG)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger

# Example usage
logger = setup_logging()
logger.debug("started up")

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
    logger.debug(f"Forwarding request to {url} with method {request.method}")

    resp = requests.request(method=request.method, url=url, headers=headers, data=request.get_data(), params=request.args, allow_redirects=False)

    # Log the response
    logger.debug(f"Received {resp.status_code} response from the upstream server")

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]

    # Correctly set headers for the response
    response = Response(resp.content, resp.status_code)
    logger.debug(f"response : {resp.content}")
    for header in headers:
        response.headers[header[0]] = header[1]

    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
