# FastApi server
import base64
import hmac
import hashlib
import json

from typing import Optional

from fastapi import FastAPI, Form, Cookie, Body
from fastapi.responses import Response


app = FastAPI()

SECRET_KEY = "f965761a5de3625ec3a1bfec4838f7cd4abc7b7db63f74a3a0b64bddb79735af"
PASSWORD_SALT = "3e0153433be7b9b9ec2e377c275f9caa0ed99c13902347a12c9227af19609894"

def sing_data(data: str) -> str:
    """Повертає підписані данні data"""
    return hmac.new(
        SECRET_KEY.encode(),
        msg=data.encode(),
        digestmod=hashlib.sha256
    ).hexdigest().upper()

def get_username_from_signed_string(username_signed: str) -> Optional[str]:
    username_base64, sign = username_signed.split(".")
    username = base64.b64decode(username_base64.encode()).decode()
    valid_sign = sing_data(username)
    if hmac.compare_digest(valid_sign, sign):
        return username

def verify_password(username: str, password: str) -> bool:
    password_hash = hashlib.sha256((password + PASSWORD_SALT).encode()).hexdigest().lower()
    stored_password_hash = users[username]["password"].lower()
    return password_hash == stored_password_hash

users = {
    "igknyaz@ukr.net": {
        "name": "Ігор",
        "password": "5a9874fa5c3c33b24ec461b8f4b965cfba8bde92a2e9d3973343169523d19c2b",
        "balance": 100_000
    },
    "ic81ic@ukr.net": {
        "name": "Інна",
        "password": "fcbb2019d68fd7b199347237484e50003bbad8c6cbae3056520fcf3f6e0f41ae",
        "balance": 555_555
    }
}

@app.get("/")
def index_page(username: Optional[str] = Cookie(default=None)):
    with open('templates/login.html', 'r', encoding="utf-8") as f:
        login_page = f.read()
    if not username:
        return Response(login_page, media_type='text/html')
    valid_username = get_username_from_signed_string(username)
    if not valid_username:
        response = Response(login_page, media_type='text/html')
        response.delete_cookie(key="username")
        return response


    try:
        user = users[valid_username]
    except KeyError:
        response = Response(login_page, media_type='text/html')
        response.delete_cookie(key="username")
        return response
    return Response(
        f"Привіт, {users[valid_username]['name']}!<br />"
        f"Баланс: {users[valid_username]['balance']}",
        media_type='text/html')



@app.post("/login")
def procces_login_page(data: dict = Body(...)):
    username = data["username"]
    password = data["password"]
    user = users.get(username)
    if not user or not verify_password(username, password):
        return Response(
            json.dumps({
                "success": False,
                "message": "Я Вас не знаю!"
            }),
            media_type='application/json')

    response = Response(
        json.dumps({
                "success": True,
                "message": f"Привіт, {user['name']}!<br />Баланс: {user['balance']}"
            }),
        media_type='application/json')

    username_signed = base64.b64encode(username.encode()).decode() + "." + sing_data(username)
    response.set_cookie(key="username", value=username_signed)
    return response
