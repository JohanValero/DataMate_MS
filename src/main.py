import os
import openai

from flask import Flask, request, jsonify
from flask_cors import CORS
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

import dbMgr

cGOOGLE_CLIENT_ID = "988130516547-4diasclnbfg99npthc2ahoogap0eqkce.apps.googleusercontent.com"

gApp : Flask = Flask(__name__)
CORS(gApp, resources={r"/auth/*": {"origins": "http://localhost:3000"}})

@gApp.route('/hello')
def hello():
    return "Hola mundo"

def general_login(iName : str, iEmail : str, iImageUrl : str, iPlataform : str):
    # Find the user in the DB.
    vUserData : dict = dbMgr.get_user_by_plataform("GOOGLE", iEmail)

    # If the user don't exists, then registrered in DB.
    if not vUserData:
        vUserData = dbMgr.save_user(iName, iEmail, iImageUrl, iPlataform)

    # Generate the JSON response.
    vResponse = {"status": "ok", "data": vUserData}
    return vResponse

@gApp.route("/auth/google", methods = ['POST'])
def google_login():
    # Verify the Google token.
    vToken = request.json['id_token']
    vIdInfo = id_token.verify_oauth2_token(
        vToken,
        google_requests.Request(),
        cGOOGLE_CLIENT_ID
    )
    vResponse = general_login(vIdInfo["name"], vIdInfo["email"], vIdInfo["picture"], "GOOGLE")
    vResponse = jsonify(vResponse)
    vResponse.headers.add('Access-Control-Allow-Origin', '*')
    return vResponse

if __name__ == "__main__":
    vPort = os.getenv('PORT', default=None)
    print(f"Running the App in development status in port: {vPort}")
    gApp.run(
        host = '0.0.0.0',
        port = vPort,
        debug = True
    )