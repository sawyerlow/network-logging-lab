from flask import Flask, request
from datetime import datetime
import json

app = Flask(__name__)
LOG_FILE = "logs.json"
request_counts = {}  # tracks the requests per IP

# Function to log requests to logs.json
def log_request(data):
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    logs.append(data)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

# Main route
@app.route('/')
def home():
    ip = request.remote_addr
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Track the number of requests per IP
    if ip in request_counts:
        request_counts[ip] += 1
    else:
        request_counts[ip] = 1

    suspicious = False
    # Flag it as suspicious if there's more than 10 requests
    if request_counts[ip] > 10:
        suspicious = True

    log_data = {
        "timestamp": timestamp,
        "ip_address": ip,
        "method": request.method,
        "path": request.path,
        "user_agent": request.headers.get("User-Agent"),
        "request_count": request_counts[ip],
        "suspicious": suspicious
    }

    log_request(log_data)
    return "Welcome to the Network Logging Lab"

# Starting the Flask server
if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(host="0.0.0.0", port=5050)