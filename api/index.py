import requests
import random
from flask import Flask, jsonify, request

app = Flask(__name__)
title = "1EAF1"
secretkey = "6Z7J4C4GMW81TKN4A45TM3XGZU61IJS93NOXP4IWQWG48TDKMU"
applab = "OC|1101299303075069|be1560dc1831af51ccb26d6fad61126d"

def auth():
    return {"content-type": "application/json","X-SecretKey": secretkey}

@app.route("/api/PlayFabAuthentication", methods=["POST"])
def playfab_authentication():
    rjson = request.get_json()
    required_fields = ["CustomId", "Nonce", "AppId", "Platform", "OculusId"]
    missing_fields = [field for field in required_fields if not rjson.get(field)]

    if missing_fields:
        return jsonify({
            "Message": f"Missing parameter(s): {', '.join(missing_fields)}",
            "Error": f"BadRequest-No{missing_fields[0]}"
        }), 400

    if rjson.get("AppId") != settings.TitleId:
        return jsonify({
            "Message": "Request sent for the wrong App ID",
            "Error": "BadRequest-AppIdMismatch"
        }), 400

    if not rjson.get("CustomId").startswith(("OC", "PI")):
        return jsonify({
            "Message": "Bad request",
            "Error": "BadRequest-NoOCorPIPrefix"
        }), 400

    url = f"https://{settings.title}.playfabapi.com/Server/LoginWithServerCustomId"
    login_request = requests.post(
        url=url,
        json={
            "ServerCustomId": rjson.get("CustomId"),
            "CreateAccount": True
        },
        headers=settings.get_auth_headers()
    )

    if login_request.status_code == 200:
        data = login_request.json().get("data")
        session_ticket = data.get("SessionTicket")
        entity_token = data.get("EntityToken").get("EntityToken")
        playfab_id = data.get("PlayFabId")
        entity_type = data.get("EntityToken").get("Entity").get("Type")
        entity_id = data.get("EntityToken").get("Entity").get("Id")

        link_response = requests.post(
            url=f"https://{settings.title}.playfabapi.com/Server/LinkServerCustomId",
            json={
                "ForceLink": True,
                "PlayFabId": playfab_id,
                "ServerCustomId": rjson.get("CustomId"),
            },
            headers=settings.get_auth_headers()
        ).json()

        return jsonify({
            "PlayFabId": playfab_id,
            "SessionTicket": session_ticket,
            "EntityToken": entity_token,
            "EntityId": entity_id,
            "EntityType": entity_type
        }), 200
    else:
        error_details = login_request.json().get('errorDetails')
        first_error = next(iter(error_details))
        return jsonify({
            "ErrorMessage": str(first_error),
            "ErrorDetails": error_details[first_error]
        }), login_request.status_code

@app.route("/api/CachePlayFabId", methods=["POST"])
def somethingelsetodolol():
    getjson = request.get_json()
    playfab_cache[getjson.get("PlayFabId")] = getjson
    return jsonify({"Message": "Success"}), 200

@app.route("/api/TitleData", methods=["POST", "GET"])
def title_data():
    response = requests.post(url=f"https://{title}.playfabapi.com/Server/GetTitleData", headers=auth())
    if response.status_code == 200:
        return jsonify(response.json().get("data").get("Data"))
    else:return jsonify({}), response.status_code

@app.route("/api/photon", methods=["POST"])
def photonauth():
    print(f"Received {request.method} request at /api/photon")
    getjson = request.get_json()
    Ticket = getjson.get("Ticket")
    Nonce = getjson.get("Nonce")
    Platform = getjson.get("Platform")
    UserId = getjson.get("UserId")
... (152 lines left)
