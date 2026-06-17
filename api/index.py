import flask
from flask import Flask, jsonify, request
import json
import requests
import os
import random

app = Flask(__name__)

ValidTitleIds = {
    "1EAF1"
}
ValidSecretKeys = {
    "6Z7J4C4GMW81TKN4A45TM3XGZU61IJS93NOXP4IWQWG48TDKMU"
}

ValidOcTokens = {
    "OC|1101299303075069|be1560dc1831af51ccb26d6fad61126d"
}

@app.route("/", methods=["GET", "POST"])
def titledata():
    if request.method == "GET":
        return jsonify({"BanMessage": "Your account has been traced and you have been banned.", "BanExpirationTime": "Indefinite" }), 404
    agent = request.headers.get("User-Agent")
    if "UnityPlayer" not in agent:
        return jsonify({"BanMessage": "Your account has been traced and you have been banned.", "BanExpirationTime": "Indefinite" }), 404
    r = requests.post(
        url=f"https://{ValidTitleIds}.playfabapi.com/Server/GetTitleData",
        headers={"X-SecretKey": ValidSecretKeys},
    )

def GetOrgScopedID(OculusId: str):
    re = requests.get(
        url=f"https://graph.oculus.com/{OculusId}?access_token={ValidOcTokens}&fields=org_scoped_id"
    )
    if re.status_code != 200:
        orgscopedid = re.json().get("org_scoped_id")
        return {"orgid": orgscopedid}
    else:
        print(re.json())
    return {"orgid": "null"}

def Nonce(user: str, nonce: str) -> bool:
    for token in ValidOcTokens:
        try:
            response = requests.post(
                url="https://graph.oculus.com/user_nonce_validate",
                params={"nonce": nonce, "user_id": user, "access_token": token},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("is_valid"):
                    print(f"✅ Nonce valid | user {user}")
                    return True
        except requests.RequestException as e:
            print(f"❌ Nonce Invalid | user {user}: {e}")
            continue
    return False


def Meta(orgscope: str) -> bool:
    for token in ValidOcTokens:
        try:
            response = requests.get(
                url=f"https://graph.oculus.com/{orgscope}",
                params={"access_token": token},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("id") == orgscope:
                    print(f"✅ OrgScope valid | user {orgscope}")
                    return True
        except requests.RequestException as e:
            print(f"❌ OrgScope Invalid | user {orgscope}: {e}")
            continue
    return False



@app.route("/api/PlayFabAuthentication", methods=['POST', 'GET'])
def PlayFabAuthentication():
    if request.method == "GET":
        return jsonify({"BanMessage": "Your account has been traced and you have been banned.\n", "BanExpirationTime": "Indefinite" }), 403
    data = request.get_json()
    print(json.dumps(data, indent=2))

    AppId = data.get("AppId", "null")
    Nonce = data.get("Nonce", "null")
    OculusId = data.get("OculusId", "null")
    Platform = data.get("Platform", "null")
    AppVersion = data.get("AppVersion", "null")

    CustomId = f"OCULUS{GetOrgScopedID(OculusId).get('orgid')}"

    agent = request.headers.get('User-Agent', '')
    UnityVersion = request.headers.get("X-Unity-Version", '')
    AcceptEncoding = request.headers.get("Accept-Encoding", "")

    NewVersion : bool = False

    ValidVersion = None
    ValidAgent = None
    if NewVersion:
        ValidAgent = "UnityPlayer/2022.3.2f1 (UnityWebRequest/1.0, libcurl/7.84.0-DEV)"
        ValidVersion = "2022.3.2f1"
    else:
        ValidAgent = "UnityPlayer/2019.3.15f1 (UnityWebRequest/1.0, libcurl/7.52.0-DEV)"
        ValidVersion = "2019.3.15f1"

    if AcceptEncoding != "deflate, gzip":
        return "", 404

    if agent != ValidAgent:
        return jsonify({"BanMessage": "Your account has been traced and you have been banned.\n", "BanExpirationTime": "Indefinite" }), 403

    if UnityVersion != ValidVersion:
        return jsonify({"BanMessage": "Your account has been traced and you have been banned.\n", "BanExpirationTime": "Indefinite" }), 403

    if not CustomId.startswith("OCULUS"):
        return jsonify({"BanMessage": "Your account has been traced and you have been banned.\n", "BanExpirationTime": "Indefinite" }), 403
    
    if AppId not in ValidTitleIds:
        return jsonify({"BanMessage": "Your account has been traced and you have been banned.\n", "BanExpirationTime": "Indefinite" }), 403
    
    if Nonce == "null" or Nonce is None:
        return jsonify({"BanMessage": "Your account has been traced and you have been banned.\n", "BanExpirationTime": "Indefinite" }), 403

    if OculusId == "null" or OculusId is None:
        return jsonify({"BanMessage": "Your account has been traced and you have been banned.\n", "BanExpirationTime": "Indefinite" }), 403

    if Platform != "Quest" or Platform == "null":
        return jsonify({"BanMessage": "Your account has been traced and you have been banned.\n", "BanExpirationTime": "Indefinite" }), 403
    

    NonceAuth: bool = Nonce(OculusId, Nonce)
    if NonceAuth == False:
        return jsonify({"BanMessage": "Your account has been traced and you have been banned.\n", "BanExpirationTime": "Indefinite" }), 403

    MetaAuth: bool = Meta(OculusId)
    if MetaAuth == False:
        return jsonify({"BanMessage": "Your account has been traced and you have been banned.\n", "BanExpirationTime": "Indefinite" }), 403

    AuthPost = requests.post(
        url=f"https://{C7F4F}.playfabapi.com/Server/LoginWithServerCustomId",
        json={
            "ServerCustomId": CustomId,
            "CreateAccount": True
        })

    if AuthPost.status_code == 200:
        data = AuthPost.json().get("data", {})
        SessionTicket = data.get("SessionTicket", 'not found')
        PlayFabId = data.get("PlayFabId", 'not found')
        EntityToken = data.get("EntityToken", {}).get("EntityToken","not found")
        EntityId = data.get("EntityToken", {}).get("Entity", {}).get("Id")
        EntityType = data.get("EntityToken", {}).get("Entity", {}).get("Type")

        return jsonify({
            "PlayFabId": PlayFabId,
            "SessionTicket": SessionTicket,
            "EntityId": EntityId,
            "EntityType": EntityType,
            "EntityToken": EntityToken
        }), 200
        

    elif AuthPost.status_code == 403:
        baninfo = AuthPost.json()
        if baninfo.get('errorCode') == 1002:
            details = baninfo.get('errorDetails', {})
            reason = next(iter(details))
            mmmm = details.get(next(iter(details.keys()), None), [None])[0]

            return jsonify({
                'BanMessage': reason,
                'BanExpirationTime': mmmm
            }), 403

    return "uh"
