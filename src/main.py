import os
import openai

from flask import Flask, request, Response, jsonify
from flask_cors import CORS
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

import dbMgr

cGOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

gApp : Flask = Flask(__name__)
CORS(gApp, resources={r"/*": {"origins": "http://localhost:3000"}})

@gApp.route('/hello')
def hello():
    return "Hola mundo"

def error_response(iError_Id : int, iError_Message : str, iSystemMessage : str) -> Response :
    vResponse : dict     = {"status": "ERROR", "message_id": iError_Id, "message": iError_Message, "system_message": iSystemMessage}
    vResponse : Response = jsonify(vResponse)
    vResponse.headers.add('Access-Control-Allow-Origin', '*')
    return vResponse

def general_login(iName : str, iEmail : str, iImageUrl : str, iPlataform : str):
    # Find the user in the DB.
    vUserData : dict = dbMgr.get_user_by_plataform("GOOGLE", iEmail)

    # If the user don't exists, then registrered in DB.
    if not vUserData:
        vUserData = dbMgr.save_user(iName, iEmail, iImageUrl, iPlataform)

    # Generate the JSON response.
    vResponse : dict = {"status": "OK", "user_data": vUserData}
    vResponse : Response = jsonify(vResponse)
    vResponse.headers.add('Access-Control-Allow-Origin', '*')
    return vResponse

@gApp.route("/auth/google", methods = ['POST'])
def google_login():
    try:
        # Verify the Google token.
        vToken = request.json['id_token']
        vIdInfo = id_token.verify_oauth2_token(vToken, google_requests.Request(), cGOOGLE_CLIENT_ID)

        # Login or Logup of the user.
        vResponse : Response = general_login(vIdInfo["name"], vIdInfo["email"], vIdInfo["picture"], "GOOGLE")
    except Exception as ex:
        print("Error during login: ", ex)
        vResponse : Response = error_response("-1", "Login failed", str(ex))
    return vResponse

@gApp.route("/api/google/get_schemas", methods = ['GET', 'POST'])
def get_schemas():
    # Verify the Google token.
    vToken = request.json['id_token']
    vUserPk = int(request.json['user_id'])
    
    try:
        vIdInfo = id_token.verify_oauth2_token(vToken, google_requests.Request(), cGOOGLE_CLIENT_ID)
    except Exception as ex:
        return error_response(1, "Authentication failed", str(ex))

    try:
        # Verify that the user is registrered in the database.
        if not dbMgr.verify_email_user_id(vUserPk, vIdInfo['email']):
            return error_response(1, "User not correctly registrered.")
        
        # Here want in the Data base or Cloud Storage the schemas saved by the user.
        vSchemas = [{
            'id': 1,
            'type': 'default',
            'name': 'Netflix\'s movies dataset'
        }, {'id': 2,
            'type': 'own',
            'name': 'Penguin\'s position'
        }]

        # Login or Logup the user.
        vResponse : dict = {'status': 'OK', 'schemas': vSchemas}
        vResponse : Response = jsonify(vResponse)
        vResponse.headers.add('Access-Control-Allow-Origin', '*')
    except Exception as ex:
        return error_response("-1", "Uncontrolled error", str(ex))
    return vResponse

if __name__ == "__main__":
    vPort = os.getenv('PORT', default=None)
    print(f"Running the App in development status in port: {vPort}")
    gApp.run(
        host = '0.0.0.0',
        port = vPort,
        debug = True
    )