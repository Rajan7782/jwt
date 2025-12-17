from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_jwt_token(uid, password):
    url = f"https://api.freefireservice.dnc.su/oauth/account:login?data={uid}:{password}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json().get("8")
    except:
        pass
    return None


@app.route("/")
def home():
    return "JWT API is running"


@app.route("/generate-jwt")
def generate_jwt():
    uid = request.args.get("uid")
    password = request.args.get("password")

    if not uid or not password:
        return jsonify({"status": 0, "error": "uid & password required"}), 400

    token = get_jwt_token(uid, password)
    if not token:
        return jsonify({"status": 0, "error": "JWT failed"}), 500

    return jsonify({"status": 1, "jwt_token": token})
