import os
from flask import Flask, request, jsonify
import requests
import logging
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# URL for the Weather Analysis Service
ANALYSIS_SERVICE_URL = os.getenv("WEATHER_ANALYSIS_SERVICE_URL", "http://weather-analysis-service.weather-wizard.svc.cluster.local/analyze")

# Validate critical environment variables
def validate_environment():
    if not ANALYSIS_SERVICE_URL:
        logger.error("Environment variable WEATHER_ANALYSIS_SERVICE_URL is not set.")
        raise RuntimeError("Critical environment variable WEATHER_ANALYSIS_SERVICE_URL is not set.")

validate_environment()

# Configure session with retries
session = requests.Session()
retries = Retry(total=3, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
session.mount("http://", HTTPAdapter(max_retries=retries))
session.mount("https://", HTTPAdapter(max_retries=retries))

@app.before_request
def log_request_info():
    logger.info(json.dumps({
        "method": request.method,
        "url": request.url,
        "headers": dict(request.headers),
        "body": request.get_json(silent=True)
    }))

@app.after_request
def log_response_info(response):
    logger.info(json.dumps({
        "status_code": response.status_code,
        "response_body": response.get_json(silent=True)
    }))
    return response

@app.route('/interact', methods=['POST'])
def interact():
    city = request.json.get("city")
    if not city:
        return jsonify({"error": "City is required."}), 400

    try:
        # Forward request to Weather Analysis Service
        response = session.post(ANALYSIS_SERVICE_URL, json={"city": city}, timeout=5)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch analysis: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
