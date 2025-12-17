from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_jwt_token(uid, password):
    url = f"https://api.demoservice.dnc.su/oauth/account:login?data={uid}:{password}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("8")
    except:
        pass
    return None

@app.route("/generate-jwt", methods=["GET"])
def generate_jwt():
    uid = request.args.get("uid")
    password = request.args.get("password")

    if not uid or not password:
        return jsonify({"status": 0, "error": "uid and password required"}), 400

    token = get_jwt_token(uid, password)

    if not token:
        return jsonify({"status": 0, "error": "JWT generation failed"}), 500

    return jsonify({"status": 1, "jwt_token": token})

# IMPORTANT for Vercel
def handler(event, context):
    return app(event, context)
