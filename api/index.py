import requests
import random
from flask import Flask, jsonify, request
import json
import os
import base64
from datetime import datetime, timedelta
import uuid
import logging
from typing import Dict, List, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GameInfo:
    def __init__(self):
        self.TitleId: str = "1EAF1"  # Playfab Title Id
        self.SecretKey: str = "6Z7J4C4GMW81TKN4A45TM3XGZU61IJS93NOXP4IWQWG48TDKMU"  # Playfab Secret Key
        self.ApiKey: str = "OC|1101299303075069|be1560dc1831af51ccb26d6fad61126d"  # App Api Key (Oculus/Graph API)

    def get_auth_headers(self):
        return {"content-type": "application/json", "X-SecretKey": self.SecretKey}

settings = GameInfo()
app = Flask(__name__)

# Utility function for input validation
def validate_input(data: Dict, required_fields: List[str]) -> Optional[List[str]]:
    return [field for field in required_fields if not data.get(field)]

# Utility function for generating unique session IDs
def generate_session_id() -> str:
    return str(uuid.uuid4())

# Utility function for returning CloudScript results
def return_function_json(funcname: str, funcparam: Dict = {}, playfab_id: Optional[str] = None):
    logger.info(f"Calling function: {funcname} with parameters: {funcparam} for player {playfab_id}")
    req = requests.post(
        url=f"https://{settings.TitleId}.playfabapi.com/Server/ExecuteCloudScript",
        json={
            "PlayFabId": playfab_id,
            "FunctionName": funcname,
            "FunctionParameter": funcparam
        },
        headers=settings.get_auth_headers()
    )
    if req.status_code == 200:
        result = req.json().get("data", {}).get("FunctionResult", {})
        logger.info(f"Function result: {result}")
        return jsonify(result), req.status_code
    else:
        logger.error(f"Function execution failed, status code: {req.status_code}")
        return jsonify({}), req.status_code

# Validate Oculus nonce
def get_is_nonce_valid(nonce: str, oculusId: str) -> bool:
    if not settings.ApiKey:
        return False
    req = requests.post(
        url=f'https://graph.oculus.com/user_nonce_validate?nonce={nonce}&user_id={oculusId}&access_token={settings.ApiKey}',
        headers={"content-type": "application/json"})
    return req.json().get("is_valid", False)

# GitHub codes raw URL for redeem codes
CODES_GITHUB_URL = "https://github.com/redapplegtag/backendsfrr/raw/main/codes.txt"

# Sample item IDs for code redemption
REDEEMABLE_ITEMS = ["cosmetic1", "cosmetic2", "cosmetic3", "bundle1", "skin1", "hat1", "gloves1"]

@app.route("/", methods=["POST", "GET"])
def main():
    return """
        <html>
            <head>
                <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap" rel="stylesheet">
            </head>
            <body style="font-family: 'Inter', sans-serif; background: linear-gradient(to bottom, #004d00, #00cc00); color: white; text-align: center; padding: 50px;">
                <h1 style="color: #eedd82; font-size: 48px; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
                    Wsp Broksie. This is a private backend!
                </h1>
                <p style="font-size: 18px;">Christmas Tag Backend Server Running Smoothly!</p>
                <img src="https://aicdn.picsart.com/275c6ae1-73a4-4cee-b3f5-45ccfa4499ae.png" alt="if u see this text it dont work" style="max-width: 500px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); display: block; margin: 30px auto;">
                <p style="font-size: 14px; opacity: 0.8;">Image loads when the server works!</p>
            </body>
        </html>
    """

@app.route("/api/PlayFabAuthentication", methods=["POST", "GET"])
def playfab_authentication():
    rjson = request.get_json()
    if not rjson:
        return jsonify({"error": "No JSON body"}), 400

    required_fields = ["Nonce", "AppId", "Platform", "OculusId"]
    missing_fields = validate_input(rjson, required_fields)
    if missing_fields:
        return jsonify({"Message": f"Missing parameter(s): {', '.join(missing_fields)}", "Error": f"BadRequest-No{missing_fields[0]}"},), 401

    if rjson.get("AppId") != settings.TitleId:
... (699 lines left)
