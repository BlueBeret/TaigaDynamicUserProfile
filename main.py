import os
import requests
from randomimage import randomimage
from time import sleep

USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
HOST = os.environ.get('HOST')
PROTOCOL = os.environ.get('PROTOCOL')

SLEEP = 60

API_URL = f"{PROTOCOL}://{HOST}/api/v1"


def login(username, password) -> dict:
    # login to the api
    response = requests.post(f"{API_URL}/auth", json={"username": username, "password": password, "type": "normal"})
    # return the token
    if response.status_code != 200:
        print(response.json())
        exit(1)
    return {"auth_token": response.json()["auth_token"], "refresh": response.json()["refresh"], "full_name": response.json()["full_name"]}


def change_avatar(auth_token, image_url) -> bool:
    # change avatar with local image
    r = requests.post(f"{API_URL}/users/change_avatar", headers={"Authorization": f"Bearer {auth_token}"}, files={"avatar": open(image_url, "rb")})
    if r.status_code != 200:
        print(r.json())
    return r.status_code == 200

def refresh_token(refresh_token) -> str:
    # refresh token
    r = requests.post(f"{API_URL}/auth/refresh", json={"refresh": refresh_token})
    return r.json()


if __name__ == "__main__":
    # login to the api
    token = login(USERNAME, PASSWORD)
    print(f"Logged in as {token['full_name']}")

    failed = 0
    # change avatar every 5 minutes
    while failed < 5:
        # get random image
        image = randomimage()
        # change avatar
        if change_avatar(token["auth_token"], image):
            print("Avatar changed")
        else:
            print("Failed to change avatar")
            failed += 1
            result = refresh_token(token["refresh"])
            token["auth_token"] = result["auth_token"]
            token["refresh"] = result["refresh"]
        # sleep for 5 minutes
        sleep(SLEEP)

    print("Failed to change avatar 5 times, exiting...")
        