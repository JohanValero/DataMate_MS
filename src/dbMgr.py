import os
import mysql.connector

cDATABASE_HOST = os.getenv("DB_HOST")
cDATABASE_PORT = os.getenv("DB_PORT")
cDATABASE_USER = os.getenv("DB_USER")
cDATABASE_PASW = os.getenv("DB_PASW")
cDATABASE_SCHM = os.getenv("DB_SCHM")

def get_db_connection():
    vConnection = mysql.connector.connect(
        host = cDATABASE_HOST,
        user = cDATABASE_USER,
        password = cDATABASE_PASW,
        port = cDATABASE_PORT,
        database = cDATABASE_SCHM
    )
    return vConnection

def get_user_by_plataform(iPlataform, iEmail):
    vDBConnection = get_db_connection()
    vCursor = vDBConnection.cursor()
    vCursor.execute(
        "SELECT u.* FROM TB_USER u, TB_USER_PLATAFORM up WHERE up.FK_USER = u.PK_USER AND up.PLATAFORM = %s AND up.EMAIL = %s",
        [iPlataform, iEmail]
    )
    vResult = vCursor.fetchone()
    vCursor.close()
    vDBConnection.close()
    if vResult:
        vResult = {
            "id": vResult[0],
            "name": vResult[1],
            "email": vResult[2],
            "image_url": vResult[3]
        }
    return vResult

def verify_email_user_id(iUserPK : int, iUserEmail : str):
    vDBConnection = get_db_connection()
    vCursor = vDBConnection.cursor()
    vCursor.execute("SELECT 1 FROM TB_USER WHERE PK_USER = %s AND EMAIL = %s", [iUserPK, iUserEmail])
    vResult = vCursor.fetchone()
    vCursor.close()
    vDBConnection.close()
    return len(vResult) > 0

def save_user(iName : str, iEmail : str, iImageUrl : str, iPlataform : str):
    vDBConnection = get_db_connection()
    vCursor = vDBConnection.cursor()
    vCursor.execute("INSERT INTO TB_USER (NAME, EMAIL, IMAGE_URL) VALUES (%s, %s, %s)", [iName, iEmail, iImageUrl])
    vUserPk = vCursor.lastrowid
    vCursor.close()
    vCursor = vDBConnection.cursor()
    vCursor.execute("INSERT INTO TB_USER_PLATAFORM (FK_USER, PLATAFORM, EMAIL) VALUES (%s, %s, %s)", [vUserPk, iPlataform, iEmail])
    vCursor.close()
    vDBConnection.commit()
    vDBConnection.close()
    vUserData = {
        "id": vUserPk,
        "name": iName,
        "email": iEmail,
        "image_url": iImageUrl
    }
    return vUserData
