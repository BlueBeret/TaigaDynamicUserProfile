import os
import requests
from randomimage import randomimage

USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
HOST = os.environ.get('HOST')
PROTOCOL = os.environ.get('PROTOCOL')

API_URL = f"{PROTOCOL}://{HOST}/api/v1"


def login(username, password) -> dict:
    # login to the api
    response = requests.post(f"{API_URL}/auth", json={"username": username, "password": password, "type": "normal"})
    # return the token
    return {"auth_token": response.json()["auth_token"], "refresh": response.json()["refresh"], "full_name": response.json()["full_name"]}


def change_avatar(auth_token, image_url) -> None:
    # change avatar with local image
    r = requests.post(f"{API_URL}/users/change_avatar", headers={"Authorization": f"Bearer {auth_token}"}, files={"avatar": open(image_url, "rb")})
    return r.json()

if __name__ == "__main__":
    # login to the api
    token = login(USERNAME, PASSWORD)
    # change avatar
    img = randomimage()
    r = change_avatar(token["auth_token"], img)
    print(r)
        