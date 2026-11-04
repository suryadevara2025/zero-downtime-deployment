from flask import Flask, jsonify
import os

app = Flask(__name__)

APP_VERSION = os.getenv("APP_VERSION", "1.0")
HEALTH_STATUS = os.getenv("HEALTH_STATUS", "healthy")

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Zero Downtime Deployment",
        "version": APP_VERSION,
        "status": "Application Running Successfully"
    })

@app.route("/health")
def health():
    if HEALTH_STATUS != "healthy":
        return jsonify({
            "status": "unhealthy",
            "version": APP_VERSION
        }), 503

    return jsonify({
        "status": "healthy",
        "version": APP_VERSION
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
