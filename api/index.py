import json
import random
import requests
from flask import Flask, jsonify, request
import traceback

app = Flask(__name__)

titleider = "1EAF1"
secretkey = "6Z7J4C4GMW81TKN4A45TM3XGZU61IJS93NOXP4IWQWG48TDKMU"
ApiKey = "OC|1101299303075069|be1560dc1831af51ccb26d6fad61126d"

def GetAuthHeaders() -> dict:
    return {"Content-Type": "application/json", "X-SecretKey": secretkey}

@app.route('/api/PlayFabAuthentication', methods=['POST'])
def PlayFabAuthentication():
    rjson = request.get_json()

    Nonce: str = rjson.get("Nonce", "Null")
    CustomId: str = rjson.get("OculusId", "Null")
    Platform: str = rjson.get("Platform", "Null")

    login_request = requests.post(
        url=f"https://{titleider}.playfabapi.com/Server/LoginWithServerCustomId",
        json={
            "ServerCustomId": f"OCULUS{CustomId}",
            "CreateAccount": True
        },
        headers={
            "content-type": "application/json",
            "x-secretkey": secretkey
        }
    )

    if login_request.status_code == 200:
        data = login_request.json().get("data")
        session_ticket = data.get("SessionTicket")
        entity_token = data.get("EntityToken").get("EntityToken")
        playfab_id = data.get("PlayFabId")
        entity_type = data.get("EntityToken").get("Entity").get("Type")
        entity_id = data.get("EntityToken").get("Entity").get("Id")

        link_response = requests.post(
            url=f"https://{titleider}.playfabapi.com/Server/LinkServerCustomId",
            json={
                "ForceLink": True,
                "PlayFabId": playfab_id,
                "ServerCustomId": f"OCULUS{CustomId}",
            },
            headers={
                "Content-Type": "application/json",
                "X-SecretKey": secretkey
            }
        ).json()

        return jsonify({
            "PlayFabId": playfab_id,
            "SessionTicket": session_ticket,
            "EntityToken": entity_token,
            "EntityId": entity_id,
            "EntityType": entity_type
        }), 200

    else:
        if login_request.status_code == 403:
            ban_info = login_request.json()
            if ban_info.get('errorCode') == 1002:
                ban_message = ban_info.get('errorMessage', "No ban message provided.")
                ban_details = ban_info.get('errorDetails', {})
                ban_expiration_key = next(iter(ban_details.keys()), None)
                ban_expiration_list = ban_details.get(ban_expiration_key, [])
                ban_expiration = ban_expiration_list[0] if len(ban_expiration_list) > 0 else "No expiration date provided."
                print(ban_info)
                return jsonify({
                    'BanMessage': ban_expiration_key,
                    'BanExpirationTime': ban_expiration
                }), 403
            else:
                error_message = ban_info.get('errorMessage', 'Forbidden without ban information.')
                return jsonify({
                    'Error': 'PlayFab Error',
                    'Message': error_message
                }), 403
        else:
            error_info = login_request.json()
            error_message = error_info.get('errorMessage', 'An error occurred.')
            return jsonify({
                'Error': 'PlayFab Error',
                'Message': error_message
            }), login_request.status_code

@app.route("/", methods=["POST", "GET"])
def Rizz():
    return jsonify({
	"MOTD": "MONKE BLOCKS: SHARE MY BLOCKS\nA NEW SPACE HAS OPENED FOR SHARED BUILD'S FIND THE PASSAGE IN THE BUILDER ROOM. JOURNEY TO THE NEW AREA.\n\nSET YOUR BACKDROP, LOAD YOUR MAP OR LOAD A FRIEND'S MAP, AND WATCH IT COME TO LIFE - THE ROOM IS BIG ENOUGH FOR FRIEND'S.\n\nDREAM IT.\nBUILD IT.\nSHARE IT.",
	"BundleKioskButton": "No existing text found at this key. Enter your MOTD text here.",
	"PrivateCrittersGrabSettings": 7,
	"PublicCrittersGrabSettings": 1,
	"SeasonalStoreBoardSign": "NEW MONKE BLOCK SPACE OPEN!\n\nDREAM IT - BUILD IT\nSHARE IT",
	"VStumpMOTD": "NEW MAPS!\n\nCAPTURE THE FLAG!\nMOLTEN MAROON\nPOOLROOMS!\nGORILLA GAMES by CATCRAZE",
	"PUNErrorLogging": 0,
	"AllActiveQuests": {
		"DailyQuests": [
			{
				"selectCount": 1,
				"name": "Gameplay",
				"quests": [
					{
						"disable": false,
						"questID": 11,
						"weight": 1,
						"questName": "PLAY INFECTION",
						"questType": "gameModeRound",
						"questOccurenceFilter": "INFECTION",
						"requiredOccurenceCount": 1,
						"requiredZones": [
							"forest",
							"canyon",
							"beach",
							"mountain",
							"skyJungle",
							"cave",
							"Metropolis",
							"bayou",
							"rotating",
							"none"
						]
					},
					{
						"disable": true,
						"questID": 19,
						"weight": 1,
						"questName": "PLAY PAINTBRAWL",
						"questType": "gameModeRound",
						"questOccurenceFilter": "PAINTBRAWL",
						"requiredOccurenceCount": 1,
						"requiredZones": [
							"forest",
							"canyon",
							"beach",
							"mountain",
							"skyJungle",
							"cave",
							"Metropolis",
							"bayou",
							"rotating",
							"none"
						]
					},
					{
						"disable": false,
						"questID": 13,
						"weight": 1,
						"questName": "PLAY FREEZE TAG",
						"questType": "gameModeRound",
						"questOccurenceFilter": "FREEZE TAG",
						"requiredOccurenceCount": 1,
						"requiredZones": [
							"forest",
							"canyon",
							"beach",
							"mountain",
							"skyJungle",
							"cave",
							"Metropolis",
							"bayou",
							"rotating",
							"none"
						]
					},
					{
						"disable": false,
						"questID": 1,
						"weight": 1,
						"questName": "PLAY GUARDIAN",
						"questType": "gameModeRound",
						"questOccurenceFilter": "GUARDIAN",
						"requiredOccurenceCount": 5,
						"requiredZones": [
							"forest",
							"canyon",
							"beach",
							"mountain",
							"cave",
							"Metropolis",
							"bayou",
							"none"
						]
					},
					{
						"disable": false,
						"questID": 4,
						"weight": 1,
						"questName": "TAG PLAYERS",
						"questType": "misc",
						"questOccurenceFilter": "GameModeTag",
						"requiredOccurenceCount": 2,
						"requiredZones": [
							"none"
						]
					}
				]
			},
			{
				"selectCount": 3,
				"name": "Exploration",
				"quests": [
					{
						"disable": false,
						"questID": 5,
						"weight": 1,
						"questName": "RIDE THE SHARK",
						"questType": "grabObject",
						"questOccurenceFilter": "ReefSharkRing",
						"requiredOccurenceCount": 1,
						"requiredZones": [
							"none"
						]
					},
					{
						"disable": false,
						"questID": 9,
						"weight": 1,
						"questName": "PLAY THE PIANO",
						"questType": "tapObject",
						"questOccurenceFilter": "Piano_Collapsed_Key",
						"requiredOccurenceCount": 10,
						"requiredZones": [
							"none"
						]
					},
					{
						"disable": false,
						"questID": 14,
						"weight": 1,
						"questName": "THROW SNOWBALLS",
						"questType": "launchedProjectile",
						"questOccurenceFilter": "SnowballProjectile",
						"requiredOccurenceCount": 10,
						"requiredZones": [
							"none"
						]
					},
					{
						"disable": false,
						"questID": 15,
						"weight": 1,
						"questName": "GO FOR A SWIM",
						"questType": "swimDistance",
						"questOccurenceFilter": "",
						"requiredOccurenceCount": 200,
						"requiredZones": [
							"none"
						]
					},
					{
						"disable": false,
						"questID": 21,
						"weight": 1,
						"questName": "CLIMB THE TALLEST TREE",
						"questType": "enterLocation",
						"questOccurenceFilter": "TallestTree",
						"requiredOccurenceCount": 1,
						"requiredZones": [
							"forest"
						]
					},
					{
						"disable": false,
						"questID": 22,
						"weight": 1,
						"questName": "COMPLETE THE OBSTACLE COURSE",
						"questType": "enterLocation",
						"questOccurenceFilter": "ObstacleCourse",
						"requiredOccurenceCount": 1,
						"requiredZones": [
							"none"
						]
					},
					{
						"disable": false,
						"questID": 23,
						"weight": 1,
						"questName": "SWIM UNDER A WATERFALL",
						"questType": "enterLocation",
						"questOccurenceFilter": "UnderWaterfall",
						"requiredOccurenceCount": 1,
						"requiredZones": [
							"none"
						]
					},
					{
						"disable": false,
						"questID": 24,
						"weight": 1,
						"questName": "SNEAK UPSTAIRS IN THE STORE",
						"questType": "enterLocation",
						"questOccurenceFilter": "SecretStore",
						"requiredOccurenceCount": 1,
						"requiredZones": [
							"none"
						]
					},
					{
						"disable": false,
						"questID": 25,
						"weight": 1,
						"questName": "CLIMB INTO THE CROW'S NEST",
						"questType": "enterLocation",
						"questOccurenceFilter": "CrowsNest",
						"requiredOccurenceCount": 1,
						"requiredZones": [
							"none"
						]
					},
					{
						"disable": false,
						"questID": 26,
						"weight": 1,
						"questName": "GO FOR A WALK",
						"questType": "moveDistance",
						"questOccurenceFilter": "",
						"requiredOccurenceCount": 500,
						"requiredZones": [
							"none"
						]
					},
					{
						"disable": false,
						"questID": 28,
						"weight": 1,
						"questName": "GET SMALL",
						"questType": "misc",
						"questOccurenceFilter": "SizeSmall",
						"requiredOccurenceCount": 1,
						"requiredZones": [
							"none"
						]
					},
					{
						"disable": false,
						"questID": 29,
						"weight": 1,
						"questName": "GET BIG",
						"questType": "misc",
						"questOccurenceFilter": "SizeLarge",
						"requiredOccurenceCount": 1,
						"requiredZones": [
							"none"
						]
					},
					{
						"disable": false,
						"questID": 31,
						"weight": 1,
						"questName": "ADD A CRITTER TO YOUR COLLECTION",
						"questType": "critter",
						"questOccurenceFilter": "Collect",
						"requiredOccurenceCount": 1,
						"requiredZones": [
							"none"
						]
					},
					{
						"disable": false,
						"questID": 32,
						"weight": 1,
						"questName": "DONATE A CRITTER",
						"questType": "critter",
						"questOccurenceFilter": "Donate",
						"requiredOccurenceCount": 1,
						"requiredZones": [
							"none"
						]
					}
				]
			},
			{
				"selectCount": 1,
				"name": "Social",
				"quests": [
					{
						"disable": false,
						"questID": 2,
						"weight": 1,
						"questName": "HIGH FIVE PLAYERS",
						"questType": "triggerHandEffect",
						"questOccurenceFilter": "HIGH_FIVE",
						"requiredOccurenceCount": 10,
						"requiredZones": [
							"none"
						]
					},
					{
						"disable": false,
						"questID": 3,
						"weight": 1,
						"questName": "FIST BUMP PLAYERS",
						"questType": "triggerHandEffect",
						"questOccurenceFilter": "FIST_BUMP",
						"requiredOccurenceCount": 10,
						"requiredZones": [
							"none"
						]
					},
					{
						"disable": false,
						"questID": 16,
						"weight": 1,
						"questName": "FIND SOMETHING TO EAT",
						"questType": "eatObject",
						"questOccurenceFilter": "",
						"requiredOccurenceCount": 1,
						"requiredZones": [
							"none"
						]
					},
					{
						"disable": false,
						"questID": 30,
						"weight": 1,
						"questName": "MAKE A FRIENDSHIP BRACELET",
						"questType": "misc",
						"questOccurenceFilter": "FriendshipGroupJoined",
						"requiredOccurenceCount": 1,
						"requiredZones": [
							"none"
						]
					}
				]
			}
		],
		"WeeklyQuests": [
			{
				"selectCount": 1,
				"name": "Gameplay",
				"quests": [
					{
						"disable": false,
						"questID": 17,
						"weight": 1,
						"questName": "PLAY INFECTION",
						"questType": "gameModeRound",
						"questOccurenceFilter": "INFECTION",
						"requiredOccurenceCount": 5,
						"requiredZones": [
							"none"
						]
					},
					{
						"disable": true,
						"questID": 20,
						"weight": 1,
						"questName": "PLAY PAINTBRAWL",
						"questType": "gameModeRound",
						"questOccurenceFilter": "PAINTBRAWL",
						"requiredOccurenceCount": 5,
						"requiredZones": [
							"none"
						]
					},
					{
						"disable": false,
						"questID": 8,
						"weight": 1,
						"questName": "PLAY FREEZE TAG",
						"questType": "gameModeRound",
						"questOccurenceFilter": "FREEZE TAG",
						"requiredOccurenceCount": 5,
						"requiredZones": [
							"none"
						]
					},
					{
						"disable": false,
						"questID": 10,
						"weight": 1,
						"questName": "PLAY GUARDIAN",
						"questType": "gameModeRound",
						"questOccurenceFilter": "GUARDIAN",
						"requiredOccurenceCount": 25,
						"requiredZones": [
							"none"
						]
					},
					{
						"disable": false,
						"questID": 12,
						"weight": 1,
						"questName": "TAG PLAYERS",
						"questType": "misc",
						"questOccurenceFilter": "GameModeTag",
						"requiredOccurenceCount": 10,
						"requiredZones": [
							"none"
						]
					}
				]
			},
			{
				"selectCount": 1,
				"name": "Exploration and Social",
				"quests": [
					{
						"disable": false,
						"questID": 33,
						"weight": 1,
						"questName": "COLLECT CRITTERS",
						"questType": "critter",
						"questOccurenceFilter": "Collect",
						"requiredOccurenceCount": 5,
						"requiredZones": [
							"none"
						]
					},
					{
						"disable": false,
						"questID": 34,
						"weight": 1,
						"questName": "DONATE CRITTERS",
						"questType": "critter",
						"questOccurenceFilter": "Donate",
						"requiredOccurenceCount": 10,
						"requiredZones": [
							"none"
						]
					},
					{
						"disable": false,
						"questID": 6,
						"weight": 1,
						"questName": "THROW SNOWBALLS",
						"questType": "launchedProjectile",
						"questOccurenceFilter": "SnowballProjectile",
						"requiredOccurenceCount": 50,
						"requiredZones": [
							"none"
						]
					},
					{
						"disable": false,
						"questID": 7,
						"weight": 1,
						"questName": "GO FOR A LONG SWIM",
						"questType": "swimDistance",
						"questOccurenceFilter": "",
						"requiredOccurenceCount": 1000,
						"requiredZones": [
							"none"
						]
					},
					{
						"disable": false,
						"questID": 18,
						"weight": 1,
						"questName": "EAT FOOD",
						"questType": "eatObject",
						"questOccurenceFilter": "",
						"requiredOccurenceCount": 25,
						"requiredZones": [
							"none"
						]
					},
					{
						"disable": false,
						"questID": 27,
						"weight": 1,
						"questName": "GO FOR A LONG WALK",
						"questType": "moveDistance",
						"questOccurenceFilter": "",
						"requiredOccurenceCount": 2500,
						"requiredZones": [
							"none"
						]
					}
				]
			}
		]
	},
	"AnnouncementData": {
		"ShowAnnouncement": "false",
		"AnnouncementID": "kID_Prelaunch",
		"AnnouncementTitle": "IMPORTANT NEWS",
		"Message": "We're working to make Gorilla Tag a better, more age-appropriate experience in our next update. To learn more, please check out our Discord."
	},
	"PrivacyPolicy_2024.10.15": "Below is our Privacy Policy. It’s important because it explains how we use your information. To make it easier, we’ll quickly explain what information we may use about you. We may get this information from you, from others like your game publisher, or from cookies. We may share this information with others to help us run and improve the game. \n\n<indent=6%>Gorilla Tag: When you play Gorilla Tag, we may use your usernames, email, online IDs, IP address, hardware information, date of birth, country, and state. We may also know what in-game items you buy and how you play the game, including your game settings and parental controls. To play the game, we may track your hand and head movements and record your voice.</indent>\n\n<indent=6%>Orion Drift: When you play Orion Drift, we may use your username, online IDs, and IP address. We may also know what in-game items you buy and how you play the game. To play the game, we may track your hand and head movements and record your voice.</indent>\n\n<indent=6%>Websites: When you visit our websites, we may track how you interact with our websites and use your IP address and online IDs.</indent>\n\n<indent=6%>Discord Channels: When you use our game Discord channels, we may use your Discord username and ID, email, and any information you share publicly.</indent>\n\n<indent=6%>Other: If you contact us directly, we will know any information you provide to us. We may collect other information about you if you sign an agreement with us.</indent>\n\n<size=60>PRIVACY POLICY AND NOTICE AT COLLECTION</size>\nLast Updated: October 15, 2024\n \nAnother Axiom Inc., a Delaware corporation (“Another Axiom”, “we,” “us,” “our,” and their derivatives) provides Gorilla Tag™, Orion Drift™, and other video games, including any playtest program (collectively, our “Games”), websites, including https://www.gorillatagvr.com/ and https://www.anotheraxiom.com/ and their respective subdomains (collectively, our “Websites”), and other online services (with our Games and Websites, collectively, our “Services”).\n\n<size=60>What does this Policy cover?</size>\n\nThis Privacy Policy and Notice at Collection (this “Policy”) sets forth how we collect, use, protect, store, disclose, and otherwise process your Personal Information (defined in Section 3 below). This Policy does NOT apply to information you provide to any third party or is collected by any third party (except as otherwise provided below). \n\nBy using our Services, you are confirming that you understand English well enough to understand this Policy. Should you have questions about this Policy, please contact us by completing a support ticket at https://support.gorillatagvr.com/ or emailing us at support@anotheraxiom.com, so we can clarify and address your questions.\n\n<size=60>How do we process Children’s Personal Information?</size>\n\nA “Child” is a person under the age needed to consent to the processing of Personal Information in their country of residence (for example, 13 years old in the United States and between 13 and 16 years old in the European Union).\n\n<size=54>Age Restrictions for Orion Drift</size>\n\nWe do not knowingly collect Personal Information from a Child. If you are a Child, do not submit any Personal Information to us. If you become aware that a Child has provided us with Personal Information, please email us at support@anotheraxiom.com, so we may delete their Personal Information.\n\n<size=54>Age Restrictions for Gorilla Tag</size>\n\nIn accordance with the policies of Valve®, Gorilla Tag is available to Steam® users at least 13 years of age. In accordance with the policies of Sony®, Gorilla Tag is available to PlayStation® users under 13 years of age only if parental consent has been provided to Sony. In accordance with the policies of Meta®, Gorilla Tag is available to Quest Pro, Quest 2, Quest 3, and next-gen headset users at least 10 years of age who access Gorilla Tag using a Parent-Managed Account, and Quest 1 and Rift® users at least 13 years of age. We do not administer Parent-Managed Accounts. For more information on creating and managing Parent-Managed Accounts, please review Meta’s education hub at https://www.meta.com/quest/safety-center/parental-supervision/. \n\nIf you become aware of an underage user, or a user who has accessed Gorilla Tag without using a Parent-Managed Account as required by Meta or without parental consent as required by Sony, please complete a support ticket at https://support.gorillatagvr.com/ or email us at support@anotheraxiom.com, so we may delete their Personal Information.\n\n<size=54>Permitted Child Users of Gorilla Tag</size>\n\nThe Personal Information we collect from or about Child users is used to give them access to certain features of Gorilla Tag and communicate with a parent or legal guardian about that Child user’s registration, including for the purpose of verifying their information in connection with the registration. \n\nIf you self-identify or are identified as a Child, your gameplay experience in Gorilla Tag will automatically be restricted. For example, unless your parent or legal guardian permits otherwise, you will be (a) restricted from communicating with or otherwise making your Personal Information publicly available to other users of Gorilla Tag by using only monkey sounds to communicate, (b) assigned randomly-generated name badges, (c) prohibited from joining private servers using room codes, and (d) restricted from purchasing in-game items.\n\nWe do not share or otherwise disclose Child users’ Personal Information, except (a) as may be necessary to protect the safety of a Child, including by disclosing their Personal Information, where appropriate, to law enforcement agencies or for an investigation related to public safety, (b) to enable us to take precautions against liability, (c) to protect the integrity, safety, and security of Gorilla Tag, or (d) where required to do so by law or legal process.\n\nAt any time, a parent or legal guardian may review their Child’s Personal Information retained by us, require us to correct or delete such Personal Information, request that we delete their Child’s account, and/or refuse to permit us from further collecting or using their Child’s Personal Information by completing a support ticket at https://support.gorillatagvr.com/ or emailing us at support@anotheraxiom.com. To protect parents and legal guardians’ privacy and security and the privacy and security of Child users, we may require a parent or legal guardian to take certain steps or provide additional information, which we will keep strictly confidential, to verify their identity before we provide any information about the Child or take the requested actions.\n\n<size=54>Kidentify Pte. Ltd.</size>\n\nGorilla Tag is provided and operated by us. However, some functionalities of Gorilla Tag, including the parent portal and contact with parents for purposes of obtaining verified parental consent and informing parents of their Child user’s online activities, are operated by Kidentify Pte. Ltd. (“k-ID”). \n\nIf you self-identify or are identified as a Child, you will first be subject to a parental notice and verified parental consent process in compliance with the Children’s Online Privacy Protection Act of 1998 and its rules (“COPPA”). \n\nTo initiate that registration and consent process, we may provide to k-ID your country, state, Internet Protocol address, and PlayFab ID and associated third party IDs from Sony, Meta, and Valve. We may share with or receive from k-ID your date of birth and email address, including your parent or legal guardian’s email address. k-ID may collect additional Personal Information from you or your parent or legal guardian such as payment, identification card, or biometric information, but we do not have access to that Personal Information.  \n\nk-ID is a valid licensee, and participating member, of the Entertainment Software Rating Board’s Privacy Certified Program (“ESRB Privacy Certified”). To protect your privacy, k-ID has voluntarily undertaken this privacy initiative, and its services have been reviewed by ESRB Privacy Certified to meet established online information collection, use, and disclosure practices. As a licensee of this privacy program, k-ID’s services are subject to audits and other enforcement and accountability mechanisms administered independently by ESRB Privacy Certified.\n\nYou may contact k-ID directly at https://www.k-id.com/contact or contact@k-id.com for any questions related to their use of your Personal Information. k-ID’s privacy policy can be found at https://www.k-id.com/privacy-policy.\n\n<size=60>What categories of Personal Information do we collect?</size>\n\nWe may collect different types of information from you depending on how you use our Services, including Personal Information. “Personal Information” means information that relates to an identified or identifiable natural person. The categories of Personal Information we may collect are listed below. Certain types of Personal Information may fall under more than one category. \n\nExcepting Personal Information of Children users of Gorilla Tag, we do not knowingly or intentionally process any sensitive Personal Information.\n\nWe may also collect information that does not generally identify you but may become associated with your account. We may use information that does not identify you for any permissible business or operational purpose under applicable law.\n\n<size=54>Gorilla Tag</size>\n\nWhen you play Gorilla Tag, we may process your: \n\n<indent=6%>Identifiers: usernames (Gorilla Tag username and Steam username), email address, unique or online IDs (such as third party IDs from Sony, Meta, Valve, and Microsoft® (Azure PlayFab®)), Internet Protocol address, and hardware ID and hardware information;</indent>\n\n<indent=6%>Geolocation: country and state;</indent>\n\n<indent=6%>Commercial information: purchase history of in-game items and DLCs;</indent>\n\n<indent=6%>Internet or other similar network activity: gameplay information and game settings and preferences, including parental controls and language;</indent>\n\n<indent=6%>Audio, electronic, visual, thermal, olfactory, or similar information: movement data (tracking your hands and head) and voice data (not voiceprints);</indent>\n\n<indent=6%>Protected classification characteristics under California or federal law: date of birth; and</indent>\n\n<indent=6%>Other: Meta age category (i.e., child, teen, or adult) and information from the content that you send to us directly by submitting a support ticket.</indent>\n\n<size=54>Orion Drift</size>\n\nWhen you play Orion Drift, we may process your: \n\n<indent=6%>Identifiers: Meta username, unique or online IDs (such as third party IDs from Epic® and Meta), and Internet Protocol address;</indent>\n\n<indent=6%>Commercial information: purchase history of in-game items and DLCs;</indent>\n\n<indent=6%>Internet or other similar network activity: gameplay information and game settings and preferences; and</indent>\n\n<indent=6%>Audio, electronic, visual, thermal, olfactory, or similar information: movement data (tracking your hands and head) and voice data (not voiceprints).</indent>\n\n<size=54>Websites</size>\n\nWhen you visit our Websites, we may process your: \n\n<indent=6%>Identifiers: first and last name and email address by completing the “Contact Us” form on our Websites, unique or online IDs (such as a third party ID from Google®), and Internet Protocol address;</indent>\n\n<indent=6%>Internet or other similar network activity: interaction with our Websites;</indent>\n\n<indent=6%>Personal Information categories listed in the California Customer Records statute (Cal. Civ. Code § 1798.80(e)): first and last name by completing the “Contact Us” form on our Websites; and</indent>\n\n<indent=6%>Other: information from the content that you send to us directly by completing the “Contact Us” form on our Websites.</indent>\n\n<size=54>Discord® Channels for our Games</size>\n\nWhen you visit Discord channels for our Games, we may process your: \n\n<indent=6%>Identifiers: Discord username, Discord user ID, and email address; and</indent>\n\n<indent=6%>Other: information from the content that you share publicly on Discord.</indent>\n\n<size=54>Modding for Gorilla Tag</size>\n\nWhen you use the Modding Tools (defined in our Fan Content & Mod Policy) for Gorilla Tag, we may process your: \n\n<indent=6%>Identifiers: usernames (Gorilla Tag username, Steam username, and mod.io username).</indent>\n\n<size=54>Content Creator Program</size>\n\nWhen you participate in our content creator program, we may process the Personal Information you provide in connection with that program, which may include your:\n\n<indent=6%>Identifiers: first and last name, usernames, social media account information, mailing address, and email address; and</indent>\n\n<indent=6%>Personal Information categories listed in the California Customer Records statute (Cal. Civ. Code § 1798.80(e)): payment and tax information, first and last name, and mailing address.</indent>\n\n<size=54>Other</size>\n\nWhen you enter into a separate written agreement with Another Axiom, we may process the Personal Information you provide in connection with that agreement, which may include your:\n\n<indent=6%>Identifiers: first and last name, email address, and usernames; and</indent>\n\n<indent=6%>Personal Information categories listed in the California Customer Records statute (Cal. Civ. Code § 1798.80(e)): first and last name.</indent>\n\nWhen you submit an Opt-Out Notice for the Arbitration Agreement described in our Terms of Service, we may process the Personal Information you provide in connection with that opt-out, which may include your:\n\n<indent=6%>Identifiers: first and last name, mailing address, and email address; and</indent>\n\n<indent=6%>Personal Information categories listed in the California Customer Records statute (Cal. Civ. Code § 1798.80(e)): first and last name, mailing address, and signature.</indent>\n\nWhen you submit a DMCA Notice or Counter-Notice described in our Fan Content & Mod Policy, we may process the Personal Information you provide in connection with that notice, which may include your:\n\n<indent=6%>Identifiers: first and last name, mailing address, and email address; and</indent>\n\n<indent=6%>Personal Information categories listed in the California Customer Records statute (Cal. Civ. Code § 1798.80(e)): first and last name, telephone number, mailing address, and signature.</indent>\n\n<size=60>From what sources do we collect Personal Information?</size>\n\n<size=54>Directly From You</size>\n\nWe may collect your Personal Information when you provide it to us directly, including the examples below.\n\n<indent=6%>When you play our Games, we may collect your movement data (tracking your hands and head), voice data (not voiceprints), gameplay information, and game settings and preferences, including parental controls and language.</indent>\n\n<indent=6%>When you contact us through the “Contact Us” form on our Websites, we may collect your first and last name, email address, and records and copies of your correspondence.</indent>\n\n<indent=6%>When you submit a support ticket, we may collect your email address and records and copies of your correspondence.</indent>\n\n<indent=6%>When you participate in a playtest for our Games, we may collect your Game or Discord username.</indent>\n\n<indent=6%>When you open Gorilla Tag, we may collect your date of birth.</indent>\n\n<indent=6%>When you self-identify or are identified as a Child user of Gorilla Tag, we may collect your parent or legal guardian’s email address.</indent>\n\n<indent=6%>When you respond to a survey or questionnaire, we may collect the information you provide.</indent>\n\n<size=54>Automatically From You</size>\n\nWe may collect your Personal Information automatically as you use our Services. For example, we may collect your Personal Information as you interact with our Websites or as you play our Games. For more information about our and third parties’ use of cookies and other automatic data collection technologies and certain choices we offer to you with respect to them, please see Section 5 below.\n\n<size=54>From Third Parties</size>\n\nWe may receive your Personal Information from or through third parties that help us provide or facilitate your access to our Services. For example, we may receive your Personal Information from the below third parties. \n\n<indent=6%>Game publishers of Orion Drift such as Meta: When you play Orion Drift, we may receive your Meta username, and when you purchase in-game items or DLCs, we may receive your purchase history. By way of another example, in connection with a ban, we may receive your Meta ID.</indent>\n\n<indent=6%>Game publishers of Gorilla Tag such as Sony, Meta, and Valve: When you play Gorilla Tag or you self-identify or are identified as a Child user, we may receive your Meta age category (i.e., child, teen, or adult), and when you purchase in-game items or DLCs, we may receive your purchase history. By way of another example, when you submit a support ticket for Gorilla Tag, we may receive your Meta ID.</indent>\n\n<indent=6%>Backend providers of Orion Drift such as Epic Games® (Online Services): When you play Orion Drift, we may receive your Epic ID.</indent>\n\n<indent=6%>Backend providers of Gorilla Tag such as Microsoft (Azure PlayFab): When you play Gorilla Tag or self-identify or are identified as a Child user, we may receive your country, state, and PlayFab ID and associated third party IDs from Sony, Meta, and Valve.</indent> \n\n<indent=6%>Social media platforms such as Discord: When you join our Games’ Discord channels, we may receive your Discord username, user ID, and the information that you share publicly on those Discord channels. When you appeal against being banned from our Games’ Discord channels, we may receive your email address.</indent> \n\n<indent=6%>Modding platforms such as mod.io®: When you use the Modding Tools (defined in our Fan Content & Mod Policy) for Gorilla Tag, we may receive your mod.io username.</indent>\n\n<indent=6%>Content creator program contractors such as Virtualities, Inc.: When you participate in our content creator program, we may receive your first and last name, usernames, social media account information, mailing address, email address, and payment and tax information.</indent>\n\n<indent=6%>Parental and legal guardian consent management provider, k-ID: When you register with k-ID as a Child user of Gorilla Tag, we may receive your date of birth and email address, including your parent or legal guardian’s email address.</indent>\n\n<indent=6%>Other users of our Games: If a user reports to us that you are violating our Terms of Service or other community policies, we may collect the information provided by that user about you. If you are a parent or legal guardian of a Child user of Gorilla Tag, we may receive your email address from your Child.</indent>\n\nWe abide by this Policy when we use Personal Information provided to us by third parties. However, we may not control the Personal Information that third parties collect or how they use that Personal Information. You should review the third parties’ privacy policies for more information about how they collect, use, and share the Personal Information they obtain and use. \n\n<size=60>How do we and third parties use cookies and other automatic data collection technologies?</size>\n\nCookies are small pieces of text sent to your browser by a website you visit. They help that website remember information about your visit, which can both make it easier to visit the site again and make the site more useful to you. \n\n<size=54>Our Cookies and Other Automatic Data Collection Technologies</size>\n\nWe may use cookies and other automatic data collection technologies on our Services to collect Personal Information, for example, regarding your interaction with our Websites. By way of another example, when you play Gorilla Tag, we may automatically collect your Internet Protocol address, hardware ID, and hardware information, and when you play Orion Drift, we may automatically collect your Internet Protocol address. When you self-identify or are identified as a Child user of Gorilla Tag, we may automatically collect your Internet Protocol address.\n\n<size=54>Third Party Cookies and Other Automatic Data Collection Technologies</size>\n\nCookies and other automatic data collection technologies on our Services may come from third parties as listed below. These cookies and other automatic data collection technologies improve your experience by helping us better tailor our Services to you. \n\nGoogle Analytics and YouTube®: Google Analytics is a web analysis service and YouTube is a video sharing and social media platform of Google Inc., 1600 Amphitheatre Parkway, Mountain View, CA 94043, United States. The Personal Information collected by Google in connection with your use of our Websites is transmitted to a server of Google in the United States, where it is stored and analyzed. Google’s collection and use of Personal Information is subject to Google's privacy policy: www.google.com/policies/privacy/partners/.\n\n<size=54>Choices about Cookies</size>\n\nYou may set your browser to refuse all or some browser cookies or to alert you when cookies are being sent (for Google: https://tools.google.com/dlpage/gaoptout). Please note that, if you disable or refuse cookies or other automatic data collection technologies, some aspects of our Services may be inaccessible or not function properly.\n\n<size=60>For what purposes do we collect your Personal Information?</size>\n\nWe may collect your Personal Information for the below purposes. \n\n<indent=6%>To provide or improve our Services: We may use your Personal Information to process your requests to access our Services and certain of their features and to generally present and improve our Services. For example, we may use your Personal Information to create your account for our Games, to grant you access to our Games, to fulfill in-game purchases, and to improve our Games or Websites.</indent>\n\n<indent=6%>To administer our Services: We may use your Personal Information for any lawful business or operational purpose in connection with administering our Services. For example, if you reach out to us, we may use your Personal Information to respond to support tickets or business inquiries sent by you.</indent>\n\n<indent=6%>To market our Services: We may use your Personal Information to market our Services to you. For example, with your prior consent, we may share news and updates about our Services through our Games’ Discord channels.</indent>\n\n<indent=6%>In furtherance of legal and safety objectives: We may access, use, and share with others your Personal Information for purposes of safety and other matters in the public interest. We may also provide access to your Personal Information to cooperate with official investigations or legal proceedings (e.g., in response to subpoenas, search warrants, court orders, or other legal processes). We may also provide access to your Personal Information to protect our rights and property and those of our agents, users, and others, including to enforce our agreements, policies, and our Terms of Service. For example, we may use your Personal Information to respond to inappropriate or reported conduct in-game, to enforce user bans for our Games and Games’ Discord channels, and for moderation and enforcement of Discord channel policies.</indent>\n\n<indent=6%>In connection with a sale or other transfer of our business: In the event all or some of our assets are sold, assigned, or transferred to or acquired by another company due to a sale, merger, divestiture, restructuring, reorganization, dissolution, financing, bankruptcy, or otherwise, your Personal Information may be among the transferred assets.</indent>\n\n<indent=6%>As we may describe to you when collecting your Personal Information: There may be other situations when we collect your Personal Information and simultaneously describe the purpose for that collection.</indent>\n\n<size=54>Lawful Basis</size>\n\nWe only collect, use, or store your Personal Information for a lawful basis such as: \n\n<indent=6%>you voluntarily provide it to us with your specific, informed, and unambiguous consent (for example, through our Games’ Discord channels);</indent>\n\n<indent=6%>it is necessary to provide you with a Service that you have requested (for example, providing you access to our Games);</indent>\n\n<indent=6%>we have a legitimate business interest that is not outweighed by your privacy rights (for example, to ban users); or</indent>\n\n<indent=6%>it is necessary to protect your vital interests or the vital interests of others (for example, where necessary to protect the safety of one of our users or someone else).</indent>\n\n<size=60>In what situations do we disclose your Personal Information?</size>\n\nWe may disclose your Personal Information to a third party, such as a service provider or contractor for a business or operational purpose, or with your consent. When we disclose Personal Information for a business or operational purpose, we enter into a contract with the service provider or contractor that describes the purpose and requires the service provider or contractor to both keep that Personal Information confidential and not use it for any purpose except performing the contract. These service providers and contractors may include our:\n\n<indent=6%>parental and legal guardian consent management provider, k-ID;</indent>\n\n<indent=6%>backend platform service providers such as Epic Games® (Online Services), Gameye, Inc., BugSplat, LLC, Unity Technologies SF (Vivox®), Microsoft (Azure PlayFab), Exit Games Inc. (Photon®), and Sauce Labs Inc.;</indent>\n\n<indent=6%>cloud computing services such as Amazon Web Services® and Google Cloud;</indent>\n\n<indent=6%>IT and security service providers such as Cloudflare, Inc. and Startup.security;</indent>\n\n<indent=6%>content creator program providers such as Zebra Partners LLC;</indent>\n\n<indent=6%>communication providers such as Slack Technologies, LLC and Google Inc. (Gmail®);</indent>\n\n<indent=6%>game analytics providers such as Hound Technology, Inc. (Honeycomb.io);</indent>\n\n<indent=6%>moderators such as GGWP and those on Discord;</indent>\n\n<indent=6%>player support providers such as Zendesk®; and</indent>\n\n<indent=6%>co-developer contractors such as ForwardXP, Inc.</indent>\n\nWe may also disclose your Personal Information:\n\n<indent=6%>to our subsidiaries and affiliates;</indent>\n\n<indent=6%>to our lawyers, consultants, accountants, business advisors, and similar third parties who owe us duties of confidentiality;</indent>\n\n<indent=6%>to a buyer or other successor in the event of a sale, merger, divestiture, restructuring, reorganization, dissolution, or other transfer of some or all of our assets, whether as a going concern or as part of bankruptcy, liquidation, or similar proceeding, in which Personal Information retained by us pertaining to the users of our Services is among the assets transferred;</indent>\n\n<indent=6%>to comply with any court order, law, or legal process, such as responding to a government or regulatory request;\nto enforce any contract we may have in effect with you;</indent>\n\n<indent=6%>if we believe disclosure is necessary or appropriate to protect the rights, property, or safety of us, our users, or others; and</indent>\n\n<indent=6%>if you have consented to such a disclosure.</indent>\n\nWe do not sell, rent, or share your Personal Information for cross contextual behavioral or targeted advertising, automated decision-making, or profiling purposes.\n\n<size=60>How is my Personal Information protected?</size>\n\n<size=54>Our Retention, Purpose Limitation, and Security Policies</size>\n\nWe protect your Personal Information through a combination of collection, security, and retention policies.\n\n<indent=6%>Limited retention: We retain each category of Personal Information only for as long as necessary to fulfill the purposes for which the Personal Information was provided to us or, if longer, to comply with any legal obligations, to resolve disputes, and to enforce contracts. For example, we may retain Personal Information collected about you to prevent repeated violations or suspected violations of our Terms of Service if your account has been banned or your access to our Services has been disabled for any reason. To determine the appropriate retention period for Personal Information, we consider the amount, nature, and sensitivity of the Personal Information, the potential risk of harm from unauthorized use or disclosure of the Personal Information, the purposes for which we process the Personal Information and whether we can achieve those purposes through other means, and the applicable legal requirements. For example, subject to the foregoing considerations, it is our policy to delete your Personal Information if we stop operating our Games or the feature through which the Personal Information was acquired.</indent>\n\n<indent=6%>Purpose limitation: We will use your Personal Information only for our Services you choose to access and for the purposes notified to you, unless we otherwise obtain your consent. We limit the collection of Personal Information to what is adequate, relevant, and reasonably necessary for those purposes.</indent>\n\n<indent=6%>Security measures: We use reasonable security measures to ensure a level of security appropriate to the volume and nature of Personal Information processed and risk involved, considering the size, scope, and type of our business, and have implemented contractual, technical, administrative, and physical security measures designed to protect your Personal Information from unauthorized access, disclosure, use, and modification. As part of our privacy compliance processes, we review these security procedures on an ongoing basis to consider new technology and methods as necessary. However, please understand that our implementation of security measures as described in this Policy does not guarantee the security of your Personal Information. In the event of a security breach, we will notify the proper regulatory authorities and any affected users of the breach within 72 hours after we become aware of the breach to the extent required by applicable law.</indent>\n\n<size=60>Your Practices and Activities</size>\n\nYour practices and activities are likewise very important for the protection of your Personal Information. You should take certain steps to help protect your Personal Information, such as being mindful of what you share publicly in our Games or Discord channels, including the below. \n\n<indent=6%>Do not use your real name when selecting a username.</indent>\n\n<indent=6%>Do not share your real name or anything private about yourself or anyone else with other users of any Game or Discord channels.</indent>\n\n<indent=6%>Do not pick a password that is easy to guess, and do not share your password.</indent>\n\nPlease remember that we have no control over what other users do with the content of your communications and no responsibility or obligation regarding other users.\n\n<size=60>How do we treat Personal Information transferred to the United States?</size>\n\n<size=54>Place of Business</size>\n\nWe may store or process your Personal Information outside of the country where we collect the information or the country in which you reside. Our primary place of business is in the United States. You should understand that we may transfer some or all of your Personal Information to the United States to carry out certain operational and processing needs as described in this Policy.\n\n<size=54>Transfer Mechanisms</size>\n\nWhen transferring Personal Information out of foreign countries, we implement technical, organizational, and physical safeguards to protect your Personal Information. We use European Commission approved standard contractual clauses and implement related measures where required by applicable law. Please contact us if you have questions related to the relevant transfer mechanism for your Personal Information.\n\n<size=60>What rights do you have to your Personal Information?</size>\n\n<size=54>Right to Access, Correct, Delete, or Restrict Processing</size>\n\nSubject to any limitations and exceptions under applicable law, you have the right to request access to your Personal Information and exercise the below rights.\n\n<indent=6%>You have the right to correct or update certain types of Personal Information. In many cases, you can review or update your account information by accessing your account online.</indent>\n\n<indent=6%>You have the right to request deletion of your Personal Information. If you choose to have your Personal Information removed from our Services, we will carry out your request within 30 days of account verification, subject to extension, and we will only retain minimal Personal Information to document your request and the actions we took to carry out your request.</indent>\n\n<indent=6%>You have the right to restrict certain processing of your Personal Information and the right to object to some types of processing of your Personal Information.</indent>\n\n<indent=6%>You have the right to withdraw your consent at any time.</indent>\n\n<indent=6%>You have the right to lodge a complaint regarding our collection, storage, or processing of your Personal Information with a data protection supervisory authority in the country where you live or work.</indent>\n\nWe will comply with your requests in accordance with, and subject to, applicable law. For example, we are not required to delete your Personal Information if we have an overriding legitimate ground for retaining that information, such as to prevent fraud. Please note that we are legally prohibited from carrying out requested actions in some instances, including (1) when we are unable to confirm your iden... (438 KB left)
