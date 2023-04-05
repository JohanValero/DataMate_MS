import sqlite3

def get_db_connection():
    vConnection = sqlite3.connect("resources/APP_REGISTER.db")
    return vConnection

def get_user_by_plataform(iPlataform, iEmail):
    vDBConnection = get_db_connection()
    vCursor = vDBConnection.cursor()
    vCursor.execute(
        "SELECT u.* FROM TB_USER u, TB_USER_PLATAFORM up WHERE FK_USER = PK_USER AND PLATAFORM = ? AND up.EMAIL = ?",
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
    vCursor.execute("SELECT 1 FROM TB_USER WHERE PK_USER = ? AND EMAIL = ?", [iUserPK, iUserEmail])
    vResult = vCursor.fetchone()
    vCursor.close()
    vDBConnection.close()
    return len(vResult) > 0

def save_user(iName : str, iEmail : str, iImageUrl : str, iPlataform : str):
    vDBConnection = get_db_connection()
    vCursor = vDBConnection.cursor()
    vCursor.execute("INSERT INTO TB_USER (NAME, EMAIL, IMAGE_URL) VALUES (?, ?, ?)", [iName, iEmail, iImageUrl])
    vUserPk = vCursor.lastrowid
    vCursor.close()
    vCursor = vDBConnection.cursor()
    vCursor.execute("INSERT INTO TB_USER_PLATAFORM (FK_USER, PLATAFORM, EMAIL) VALUES (?, ?, ?)", [vUserPk, iPlataform, iEmail])
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
